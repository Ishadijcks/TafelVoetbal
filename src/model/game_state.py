from dataclasses import dataclass, field
from typing import Dict

from communication.commands.commands import StickId


@dataclass
class GameState:
    sticks: Dict[StickId, float] = field(default_factory=lambda: {
        StickId.ONE: 0,
        StickId.TWO: 0,
        StickId.THREE: 0,
        StickId.FOUR: 0,
    })

    ball: tuple[float, float] = field(default_factory=lambda: (0.0, 0.0))
