from serial import Serial

from communication.commands.commands import BaseCommand


class MockSerial(Serial):
    def __init__(self, port=''):
        print("Mock serial started")
        pass

    def send_commands(self, commands: list[BaseCommand]) -> None:
        pass

    def send_command(self, command: BaseCommand) -> None:
        pass
