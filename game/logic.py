from dataclasses import dataclass
from typing import Tuple
from game.config import GameConfig

@dataclass(frozen=True)
class GameState:
    board: Tuple[int, ...]
    player: int
    config: GameConfig

def init_state(config: GameConfig, stones_per_pit: int = 4) -> GameState:
    board = [stones_per_pit] * config.board_size
    board[config.p0_store] = 0
    board[config.p1_store] = 0
    return GameState(board=tuple(board), player=0, config=config)

def legal_moves(state: GameState) -> list[int]:
    b = state.board
    cfg = state.config
    return [i for i in cfg.pits_range(state.player) if b[i] > 0]


def is_terminal(state: GameState) -> bool:
    b = state.board
    cfg = state.config
    side0_empty = all(b[i] == 0 for i in cfg.pits_range(0))
    side1_empty = all(b[i] == 0 for i in cfg.pits_range(1))
    return side0_empty or side1_empty


def finalize_if_terminal(state: GameState) -> GameState:
    if not is_terminal(state):
        return state

    cfg = state.config
    b = list(state.board)

    side0_sum = sum(b[i] for i in cfg.pits_range(0))
    side1_sum = sum(b[i] for i in cfg.pits_range(1))

    for i in cfg.pits_range(0):
        b[i] = 0
    for i in cfg.pits_range(1):
        b[i] = 0

    b[cfg.primary_store(0)] += side0_sum
    b[cfg.primary_store(1)] += side1_sum

    return GameState(board=tuple(b), player=state.player, config=cfg)


def apply_move(state: GameState, pit: int) -> Tuple[GameState, bool]:
    cfg = state.config

    if pit not in cfg.pits_range(state.player):
        raise ValueError("Pit not on current player's side.")

    b = list(state.board)
    stones = b[pit]
    if stones <= 0:
        raise ValueError("Pit is empty.")

    b[pit] = 0
    idx = pit

    # Sow
    while stones > 0:
        idx = (idx + 1) % cfg.board_size
        if cfg.should_skip(state.player, idx):
            continue
        b[idx] += 1
        stones -= 1

    extra_turn = cfg.grants_extra_turn(state.player, idx)

    # Capture: last stone in empty own pit AND opposite has stones
    if (not extra_turn) and cfg.is_own_pit(state.player, idx) and b[idx] == 1:
        opp = cfg.opposite_pit(idx)
        if b[opp] > 0:
            captured = b[opp] + b[idx]
            b[opp] = 0
            b[idx] = 0
            b[cfg.primary_store(state.player)] += captured

    next_player = state.player if extra_turn else (1 - state.player)
    new_state = GameState(board=tuple(b), player=next_player, config=cfg)
    new_state = finalize_if_terminal(new_state)
    return new_state, extra_turn


def score(state: GameState) -> int:
    cfg = state.config
    return state.board[cfg.p0_store] - state.board[cfg.p1_store]


def winner(state: GameState) -> int | None:
    cfg = state.config
    b = state.board
    if b[cfg.p0_store] > b[cfg.p1_store]:
        return 0
    if b[cfg.p1_store] > b[cfg.p0_store]:
        return 1
    return None