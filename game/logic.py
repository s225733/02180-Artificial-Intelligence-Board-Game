from dataclasses import dataclass
from typing import List, Tuple

PITS_PER_SIDE = 6
BOARD_SIZE = 14
P0_STORE = 6
P1_STORE = 13


@dataclass(frozen=True)
class GameState:
    board: Tuple[int, ...]  # immutable for easy AI search
    player: int             # 0 or 1


def init_state(stones_per_pit: int = 4) -> GameState:
    board = [stones_per_pit] * BOARD_SIZE
    board[P0_STORE] = 0
    board[P1_STORE] = 0
    return GameState(board=tuple(board), player=0)


def pits_range(player: int) -> range:
    return range(0, 6) if player == 0 else range(7, 13)


def store_index(player: int) -> int:
    return P0_STORE if player == 0 else P1_STORE


def opponent_store(player: int) -> int:
    return P1_STORE if player == 0 else P0_STORE


def is_own_pit(player: int, idx: int) -> bool:
    return idx in pits_range(player)


def opposite_pit(idx: int) -> int:
    # Valid for pits only (0..5 or 7..12)
    return 12 - idx


def legal_moves(state: GameState) -> List[int]:
    b = state.board
    return [i for i in pits_range(state.player) if b[i] > 0]


def is_terminal(state: GameState) -> bool:
    b = state.board
    side0_empty = all(b[i] == 0 for i in range(0, 6))
    side1_empty = all(b[i] == 0 for i in range(7, 13))
    return side0_empty or side1_empty


def finalize_if_terminal(state: GameState) -> GameState:
    if not is_terminal(state):
        return state

    b = list(state.board)
    side0_sum = sum(b[i] for i in range(0, 6))
    side1_sum = sum(b[i] for i in range(7, 13))

    for i in range(0, 6):
        b[i] = 0
    for i in range(7, 13):
        b[i] = 0

    b[P0_STORE] += side0_sum
    b[P1_STORE] += side1_sum

    return GameState(board=tuple(b), player=state.player)


def apply_move(state: GameState, pit: int) -> Tuple[GameState, bool]:
    """
    Returns: (new_state, extra_turn)
    Enforces sowing, skipping opponent store, capture rule, and terminal sweep.
    """
    if pit not in pits_range(state.player):
        raise ValueError("Pit not on current player's side.")
    b = list(state.board)
    stones = b[pit]
    if stones <= 0:
        raise ValueError("Pit is empty.")

    b[pit] = 0
    idx = pit
    opp_store = opponent_store(state.player)

    # Sow
    while stones > 0:
        idx = (idx + 1) % BOARD_SIZE
        if idx == opp_store:
            continue
        b[idx] += 1
        stones -= 1

    extra_turn = (idx == store_index(state.player))

    # Capture
    if (not extra_turn) and is_own_pit(state.player, idx) and b[idx] == 1:
        opp = opposite_pit(idx)
        if b[opp] > 0:
            captured = b[opp] + b[idx]
            b[opp] = 0
            b[idx] = 0
            b[store_index(state.player)] += captured

    next_player = state.player if extra_turn else (1 - state.player)
    new_state = GameState(board=tuple(b), player=next_player)
    new_state = finalize_if_terminal(new_state)
    return new_state, extra_turn


def score(state: GameState) -> int:
    """Positive means P0 is ahead."""
    return state.board[P0_STORE] - state.board[P1_STORE]


def winner(state: GameState) -> int | None:
    """Returns 0 if P0 wins, 1 if P1 wins, None if tie. Call only when terminal."""
    b = state.board
    if b[P0_STORE] > b[P1_STORE]:
        return 0
    if b[P1_STORE] > b[P0_STORE]:
        return 1
    return None