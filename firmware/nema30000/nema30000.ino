#include <AccelStepper.h> 

#define STEPS 200
#define NEMA_SPEED 8000
#define NEMA_ACCELERATE 8000

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
#define TRANSLATION_RANGE 220*4

#define ROTATION_SCALE ROTATION_RANGE/200
#define TRANSLATION_SCALE TRANSLATION_RANGE/254

#define ROTATION_CALIBRATION 13
#define TRANSLATION_CALIBRATION 12

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver
AccelStepper rotation(AccelStepper::DRIVER, 2, 5); // Pin 5 connected to DIRECTION & Pin 2 connected to STEP Pin of Driver
AccelStepper translation(AccelStepper::DRIVER, 3, 6);   // Pin 6 connected to DIRECTION & Pin 3 connected to STEP Pin of Driver

void setup() {

  rotation.setMaxSpeed(NEMA_SPEED);
  rotation.setAcceleration(NEMA_ACCELERATE);
  rotation.setCurrentPosition(0);

  translation.setMaxSpeed(NEMA_SPEED);
  translation.setAcceleration(NEMA_ACCELERATE);
  translation.setCurrentPosition(0);

  pinMode(8, OUTPUT);
  digitalWrite(8, LOW);

  pinMode(ROTATION_CALIBRATION, INPUT_PULLUP);
  pinMode(TRANSLATION_CALIBRATION, INPUT_PULLUP);


  // Initiate the serial connection
  Serial.begin(9600);
  clear_buffer();

  calibrate();
}

uint8_t serial_buffer[MSG_PHRASE_LENGTH];
uint8_t buffer_index = 0;

void loop() {
  rotation.run();
  translation.run();

  if(Serial.available()>0){
    uint8_t byte = Serial.read();

    // If its the start byte, clear the buffer
    if(byte == MSG_START)
      clear_buffer();

    if(byte == MSG_CALIBRATE){
      calibrate();
      clear_buffer();
      Serial.print(MSG_OK);
    }

    serial_buffer[buffer_index] = byte;
    buffer_index++;
  
    if(buffer_index == MSG_PHRASE_LENGTH){
      parse_buffer();
      clear_buffer();
    }
  }
}

void clear_buffer(){
  memset(serial_buffer, 0, sizeof(serial_buffer));
  buffer_index = 0;
}

void parse_buffer(){

  if(serial_buffer[0] != MSG_START){
    Serial.write(MSG_ERROR);

    return;
  }
  
  if(serial_buffer[1] == MSG_ROTATE){
    uint8_t arm_index = serial_buffer[2];
    
    long position = serial_buffer[3]*ROTATION_SCALE;
    rotation.moveTo(position);
    
    Serial.write(MSG_OK);
    return;
  }

  if(serial_buffer[1] == MSG_TRANSLATE){
    uint8_t arm_index = serial_buffer[2];
    
    long position = serial_buffer[3]*TRANSLATION_SCALE;
    translation.moveTo(position);
    
    Serial.write(MSG_OK);
    return;
  }
}

void calibrate(){

  while(digitalRead(ROTATION_CALIBRATION)){
    if(rotation.distanceToGo() == 0){
      rotation.move(-5);
    }
    rotation.run();
  }
  
  rotation.setCurrentPosition(0);
  
  while(digitalRead(TRANSLATION_CALIBRATION)){
    if(translation.distanceToGo() == 0){
      translation.move(5);
    }
    translation.run();
  }
  
  translation.setCurrentPosition(TRANSLATION_RANGE);
}

