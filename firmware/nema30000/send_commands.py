from serial import Serial

port = "/dev/ttyACM1"
baud = 9600

ser = Serial(port, baud, timeout=1)
ser.reset_input_buffer()
print(f"Serial port opened on port {port}")

commands = [0xFF, 0x03, 0x00, 0x00]

for command in commands:
    ser.write(command)
    
while True:
    if ser.in_waiting > 0:
        line = ser.readline()
        print("received ", line.hex())