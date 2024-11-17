#include <AccelStepper.h> 

#define STEPS 200
#define NEMA_SPEED 200
#define NEMA_ACCELERATE 1


#define CONTROL_FREQUENCY 20
#define SPEED_RAMP_RATE 2
#define NUMBER_OF_ARMS 1

#define MSG_CALIBRATE 0x01
#define MSG_TRANSLATE 0x02
#define MSG_ROTATE    0x03
#define MSG_START     0xFF
#define MSG_OK        0x0A
#define MSG_ERROR     0x0E
#define MSG_PHRASE_LENGTH 4

#define CONTROL_TIME_MILLIS 1000/CONTROL_FREQUENCY // Delay time between PID loops


// Ranges of the motors
#define ROTATION_RANGE 255

#define ROTATION_SCALE ROTATION_RANGE/255

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver

AccelStepper rotation(AccelStepper::DRIVER, 2, 5); // Pin 5 connected to DIRECTION & Pin 2 connected to STEP Pin of Driver
AccelStepper translation(AccelStepper::DRIVER, 6, 3);   // Pin 6 connected to DIRECTION & Pin 3 connected to STEP Pin of Driver

void setup() {

  rotation.setMaxSpeed(NEMA_SPEED);
  rotation.setAcceleration(NEMA_ACCELERATE);

  pinMode(8, OUTPUT);
  digitalWrite(8,LOW);

  // Initiate the serial connection
  Serial.begin(9600);
  clear_buffer();
}

uint8_t serial_buffer[MSG_PHRASE_LENGTH];
uint8_t buffer_index = 0;

typedef struct {
  uint8_t x_position;
  uint8_t x_setpoint;
  uint8_t r_position;
  uint8_t r_setpoint;
  uint8_t speed;
  uint8_t step_range;
} player_arm_t;

player_arm_t player_arm[NUMBER_OF_ARMS];

void loop() {
  rotation.run();

  // if(Serial.available()>0){
  //   uint8_t byte = Serial.read();

  //   // If its the start byte, clear the buffer
  //   if(byte == MSG_START)
  //     clear_buffer();

  //   // if(byte == MSG_CALIBRATE){
  //   //   calibrate();
  //   //   clear_buffer();
  //   //   Serial.write(MSG_OK);
  //   // }

  //   serial_buffer[buffer_index] = byte;
  //   buffer_index++;
  
  //   if(buffer_index == MSG_PHRASE_LENGTH){
  //     parse_buffer();
  //     clear_buffer();
  //   }
  // }
}

void clear_buffer(){
  memset(serial_buffer, 0, sizeof(serial_buffer));
  buffer_index = 0;
}

void parse_buffer(){
  if(serial_buffer[0] != MSG_START){
    Serial.write(MSG_ERROR);
    for(int i=0; i<4; i++){
      Serial.print(serial_buffer[i]);
    }
    Serial.write("\n\r");

    return;
  }
  
  if(serial_buffer[1] == MSG_ROTATE){
    uint8_t arm_index = serial_buffer[2];
    rotation.moveTo(serial_buffer[3]);
    Serial.write(MSG_OK);
    return;
  }

  if(serial_buffer[1] == MSG_TRANSLATE){
    uint8_t arm_index = 0;//serial_buffer[2];
    player_arm[arm_index].x_setpoint = serial_buffer[3];
    Serial.write(MSG_OK);
    return;
  }
}

void calibrate(){
  return;
}

