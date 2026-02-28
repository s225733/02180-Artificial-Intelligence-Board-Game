from dataclasses import dataclass

@dataclass(frozen=True)
class GameConfig:
    pits_per_side: int

    @property
    def board_size(self) -> int:
        return 2 * self.pits_per_side + 2

    @property
    def p0_store(self) -> int:
        return self.pits_per_side

    @property
    def p1_store(self) -> int:
        return 2 * self.pits_per_side + 1

    def pits_range(self, player: int) -> range:
        if player == 0:
            return range(0, self.pits_per_side)
        return range(self.pits_per_side + 1, 2 * self.pits_per_side + 1)

    def opponent_store(self, player: int) -> int:
        return self.p1_store if player == 0 else self.p0_store

    def store_index(self, player: int) -> int:
        return self.p0_store if player == 0 else self.p1_store

    def is_own_pit(self, player: int, idx: int) -> bool:
        return idx in self.pits_range(player)

    def opposite_pit(self, idx: int) -> int:
        return 2 * self.pits_per_side - idx