
from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet, Optional, Tuple


@dataclass(frozen=True)
class PitProps:
    owner: Optional[int]                 # 0, 1, or None
    is_scoring: bool                     # store-like pit
    skip_for_player: FrozenSet[int]      # players who must skip this pit when sowing
    grants_extra_turn_for: FrozenSet[int]  # players who get extra turn if last stone lands here


@dataclass(frozen=True)
class GameConfig:
    pits_per_side: int
    pit_props: Tuple[PitProps, ...]      # length == board_size
    primary_store_p0: int                # captures + terminal sweep go here
    primary_store_p1: int

    @property
    def board_size(self) -> int:
        return 2 * self.pits_per_side + 2

    # Keep these for compatibility with your current code (they now mean "primary store")
    @property
    def p0_store(self) -> int:
        return self.primary_store_p0

    @property
    def p1_store(self) -> int:
        return self.primary_store_p1

    def pits_range(self, player: int) -> range:
        # Normal pits only (not scoring pits)
        if player == 0:
            return range(0, self.pits_per_side)
        return range(self.pits_per_side + 1, 2 * self.pits_per_side + 1)

    def is_own_pit(self, player: int, idx: int) -> bool:
        return idx in self.pits_range(player)

    def opposite_pit(self, idx: int) -> int:
        return 2 * self.pits_per_side - idx

    # ---- NEW generalized scoring/store behavior ----

    def scoring_pits(self, player: int) -> set[int]:
        return {
            i for i, p in enumerate(self.pit_props)
            if p.owner == player and p.is_scoring
        }

    def opponent_scoring_pits(self, player: int) -> set[int]:
        return self.scoring_pits(1 - player)

    def is_scoring_pit(self, player: int, idx: int) -> bool:
        return idx in self.scoring_pits(player)

    def should_skip(self, player: int, idx: int) -> bool:
        return player in self.pit_props[idx].skip_for_player

    def grants_extra_turn(self, player: int, idx: int) -> bool:
        return player in self.pit_props[idx].grants_extra_turn_for

    def primary_store(self, player: int) -> int:
        return self.primary_store_p0 if player == 0 else self.primary_store_p1

    def player_score(self, board: Tuple[int, ...], player: int) -> int:
        return sum(board[i] for i in self.scoring_pits(player))


def make_standard_config(pits_per_side: int) -> GameConfig:
    """
    Standard Kalah:
    indices:
      p0 pits: 0..pits_per_side-1
      p0 store: pits_per_side
      p1 pits: pits_per_side+1 .. 2*pits_per_side
      p1 store: 2*pits_per_side+1
    """
    board_size = 2 * pits_per_side + 2
    p0_store = pits_per_side
    p1_store = 2 * pits_per_side + 1

    props = []
    for i in range(board_size):
        if 0 <= i < pits_per_side:
            props.append(PitProps(owner=0, is_scoring=False,
                                  skip_for_player=frozenset(),
                                  grants_extra_turn_for=frozenset()))
        elif i == p0_store:
            props.append(PitProps(owner=0, is_scoring=True,
                                  skip_for_player=frozenset({1}),
                                  grants_extra_turn_for=frozenset({0})))
        elif pits_per_side + 1 <= i <= 2 * pits_per_side:
            props.append(PitProps(owner=1, is_scoring=False,
                                  skip_for_player=frozenset(),
                                  grants_extra_turn_for=frozenset()))
        elif i == p1_store:
            props.append(PitProps(owner=1, is_scoring=True,
                                  skip_for_player=frozenset({0}),
                                  grants_extra_turn_for=frozenset({1})))
        else:
            # Should never happen, but keep it safe.
            props.append(PitProps(owner=None, is_scoring=False,
                                  skip_for_player=frozenset(),
                                  grants_extra_turn_for=frozenset()))

    return GameConfig(
        pits_per_side=pits_per_side,
        pit_props=tuple(props),
        primary_store_p0=p0_store,
        primary_store_p1=p1_store,
    )