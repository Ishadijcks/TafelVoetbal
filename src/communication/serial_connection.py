from serial import Serial

from communication.commands.commands import BaseCommand

if __name__ == '__main__':

    ser = Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)


class SerialConnection:
    def __init__(self, port: str, baud: int = 9600):
        self.ser = Serial(port, baud, timeout=1)
        print(f"Serial port opened on port {port}")

    def send_commands(self, commands: list[BaseCommand]) -> None:
        for command in commands:
            self.send_command(command)

    def send_command(self, command: BaseCommand) -> None:
        serialized = command.serialize()
        self.ser.write(serialized)
