import math

from communication.commands.commands import BaseCommand, StickId
from communication.commands.translate_command import TranslateCommand
from model.game_state import GameState
from strategy.strategy import Strategy


class PingPongStrategy(Strategy):
    """
    Pingpongs between 0 and 1.

    Wrong sport but eh :)
    """

    def __init__(self, duration):
        super().__init__()
        self.total_time = 0.0
        self.duration = duration

    def execute(self, previous_state: GameState, state: GameState, delta: float) -> list[BaseCommand]:
        self.total_time += delta
        target_position = 0.5 + 0.5 * math.sin(self.total_time * math.pi / self.duration)
        return [
            TranslateCommand(StickId.ONE, target_position)
        ]
