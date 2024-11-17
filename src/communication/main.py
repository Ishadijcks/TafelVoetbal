from typing import Annotated

import typer

from communication.commands.commands import StickId, BaseCommand, CommandType
from communication.serial_connection import SerialConnection


def main(
        port: Annotated[str, typer.Option()] = "/dev/ttyACM0",
        type: Annotated[int, typer.Option()] = CommandType.ROTATE,
        stick_id: Annotated[int, typer.Option()] = StickId.ONE,
        data: Annotated[int, typer.Argument()] = 0x00,
):
    serial = SerialConnection(port=port)
    command = BaseCommand(
        type=CommandType(type),
        stick=StickId(stick_id),
        data=data,
    )

    print("Sending command...", command)
    serial.send_command(command)

def cli():
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
