from communication.commands.commands import BaseCommand, StickId
from communication.commands.rotate_command import RotateCommand
from communication.commands.translate_command import TranslateCommand
from model.game_state import GameState
from strategy.strategy import Strategy


class ManualInput(Strategy):
    """
    Takes manual input from a ui.

    TODO Add support for multiple sticks
    TODO Add pyqt ui
    """

    def __init__(self, initial_translate: float = 0.5, initial_rotate: float = 0.5):
        super().__init__()
        self.translate = initial_translate
        self.rotate = initial_rotate

    def execute(self, state: GameState, delta: float) -> list[BaseCommand]:
        return [
            TranslateCommand(StickId.ONE, self.translate),
            RotateCommand(StickId.ONE, self.rotate),
        ]
