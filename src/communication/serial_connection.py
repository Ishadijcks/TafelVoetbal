import time

from serial import Serial

from communication.commands.commands import BaseCommand

class SerialConnection:
    def __init__(self, port: str, baud: int = 9600):
        self.ser = Serial(port, baud, timeout=1)
        self.ser.reset_input_buffer()
        time.sleep(2)
        print(f"Serial port opened on port {port}")

    def send_commands(self, commands: list[BaseCommand]) -> None:
        for command in commands:
            self.send_command(command)

    def send_command(self, command: BaseCommand) -> None:
        serialized = command.serialize()
        self.ser.write(serialized)

        while not self.ser.in_waiting:
            pass

        if self.ser.in_waiting > 0:
            line = self.ser.read(1)

            print("expected", serialized.hex(), "received", line.hex())
