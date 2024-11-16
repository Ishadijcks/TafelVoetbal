import multiprocessing
import signal
import sys

from PyQt5.QtWidgets import QApplication

from communication.commands.commands import BaseCommand, StickId
from communication.commands.translate_command import TranslateCommand
from model.game_state import GameState
from strategy.strategy import Strategy

from ui.input_window import SliderInputWindow


class ManualInputStrategy(Strategy):
    """
    Takes manual input from a ui.

    TODO Add support for multiple sticks
    TODO Add pyqt ui
    """

    def __init__(self, initial_translate: float = 0.5, initial_rotate: float = 0.5):
        super().__init__()
        self.translate = multiprocessing.Value('f', initial_translate)
        self.rotate = multiprocessing.Value('f', initial_rotate)

        proc = multiprocessing.Process(target=self.start_ui, args=())
        proc.daemon = True
        proc.start()

        print("showing app")

    def start_ui(self):
        app = QApplication(sys.argv)
        window = SliderInputWindow(
            self.translate.value,
            self.on_translate,
            self.rotate.value,
            self.on_rotate,
        )
        window.show()
        app.exec()

    def on_translate(self, value: float) -> None:
        self.translate.value = value

    def on_rotate(self, value: float) -> None:
        self.rotate.value = value

    def execute(self, state: GameState, delta: float) -> list[BaseCommand]:

        return [
            TranslateCommand(StickId.ONE, self.translate.value),
            # RotateCommand(StickId.ONE, self.rotate.value),
        ]
