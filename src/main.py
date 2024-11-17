import time
from enum import Enum
from typing import Dict

import typer

from communication.commands.calibrate_command import CalibrateCommand
from communication.mock_serial import MockSerial
from communication.serial_connection import SerialConnection
from sensing.mock_sensor import MockSensor
from sensing.sensor import Sensor
from sensing.video_sensor import VideoSensor
from sensing.picamera import PiCamera
from strategy.follow_strategy import FollowStrategy
from strategy.manual_input_strategy import ManualInputStrategy
from strategy.ping_pong_strategy import PingPongStrategy
from strategy.strategy import Strategy


class SerialType(str, Enum):
    usb0 = "usb0"
    acm0 = "acm0"
    mock = "mock"


class StrategyType(str, Enum):
    manual = "manual"
    follow = "follow"
    pingpong = "pingpong"


class SensorType(str, Enum):
    video = "video"
    picamera = "picamera"
    mock = "mock"


sensors: Dict[SensorType, type[Sensor]] = {
    SensorType.video: VideoSensor,
    SensorType.picamera: PiCamera,
    SensorType.mock: MockSensor,
}

serials: Dict[SerialType, type[SerialConnection]] = {
    SerialType.acm0: SerialConnection,
    SerialType.usb0: SerialConnection,
    SerialType.mock: MockSerial,
}

serialports: Dict[SerialType, str] = {
    SerialType.acm0: "/dev/ttyACM0",
    SerialType.usb0: "/dev/ttyUSB0",
    SerialType.mock: "",
}

strategies: Dict[StrategyType, type[Strategy]] = {
    StrategyType.manual: ManualInputStrategy,
    StrategyType.follow: FollowStrategy,
    StrategyType.pingpong: PingPongStrategy,
}


def main(
        strategy: StrategyType = StrategyType.manual,
        serial: SerialType = SerialType.acm0,
        sensor: SensorType = SensorType.picamera,
        pingpong_duration: int = 10,
        video_path: str = '/'
):
    if sensor == SensorType.video:
        sensor: Sensor = sensors[sensor](path=video_path)
    else:
        sensor: Sensor = sensors[sensor]()

    serial: SerialConnection = serials[serial](port=serialports[serial])

    if strategy == StrategyType.pingpong:
        strategy: Strategy = strategies[strategy](duration=pingpong_duration)
    else:
        strategy: Strategy = strategies[strategy]()

    serial.send_command(CalibrateCommand())

    last_time = time.time()
    previous_state = sensor.get_state(0)

    while True:
        # Time calculations
        now = time.time()
        delta = now - last_time
        last_time = now

        # Gather state from world
        state = sensor.get_state(delta)


        # Execute strategy based on state
        commands = strategy.execute(previous_state, state, delta)
        previous_state = state
        print("Tick duration", int(1000 * delta), "ms", ', '.join([str(c) for c in commands]))

        # Send commands
        serial.send_commands(commands)


def cli():
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
