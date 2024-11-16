from abc import ABC

from model.game_state import GameState


class Sensor(ABC):

    def get_state(self, delta: float) -> GameState:
        raise NotImplementedError()
