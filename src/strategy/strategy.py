from abc import ABC, abstractmethod

from communication.commands.commands import BaseCommand
from model.game_state import GameState


class Strategy(ABC):

    @abstractmethod
    def execute(self, state: GameState, delta: float) -> list[BaseCommand]:
        raise NotImplementedError()
