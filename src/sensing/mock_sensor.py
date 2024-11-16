import math

from communication.commands.commands import StickId
from model.game_state import GameState
from sensing.sensor import Sensor


class MockSensor(Sensor):
    """
    A fake sensor that sees the ball move between the posts.
    """

    def __init__(self, duration):
        super().__init__()
        self.total_time = 0.0
        self.duration = duration

    def get_state(self, delta: float) -> GameState:
        self.total_time += delta
        return GameState(
            sticks={
                StickId.ONE: 0,
                StickId.TWO: 0,
                StickId.THREE: 0,
                StickId.FOUR: 0,
            },
            ball=(
                0.5 + 0.5 * math.cos(self.total_time * math.pi / self.duration),
                0.0
            )
        )
