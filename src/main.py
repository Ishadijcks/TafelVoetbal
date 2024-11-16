import time

from communication.mock_serial import MockSerial
from sensing.mock_sensor import MockSensor
from sensing.sensor import Sensor
from sensing.video_sensor import VideoSensor
from strategy.follow_x_strategy import FollowXStrategy
from strategy.manual_input_strategy import ManualInputStrategy
from strategy.ping_pong_strategy import PingPongStrategy
from strategy.strategy import Strategy


def main():
    last_time = time.time()

    # serial = SerialConnection("/dev/ttyUSB0")
    serial = MockSerial()

    strategy: Strategy = ManualInputStrategy()
    # strategy: Strategy = FollowXStrategy()


    # sensor: Sensor = VideoSensor("./assets/blauw.mp4")
    # sensor: Sensor = MockSensor(5)
    sender: Sensor = Vision

    while True:
        # Time calculations
        now = time.time()
        delta = now - last_time
        last_time = now

        # Gather state from world
        state = sensor.get_state(delta)

        # Execute strategy based on state
        commands = strategy.execute(state, delta)

        print("Tick duration", int(1000 * delta), "ms", ', '.join([str(c) for c in commands]))

        # Send commands
        serial.send_commands(commands)


if __name__ == "__main__":
    main()
