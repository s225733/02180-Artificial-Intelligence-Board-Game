from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from game.config import GameConfig

@dataclass(frozen=True)
class GameState:
    board: Tuple[int, ...]
    player: int
    config: GameConfig