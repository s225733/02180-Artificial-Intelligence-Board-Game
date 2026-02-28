import pytest
from game.config import GameConfig
from game.logic import (
    GameState,
    init_state,
    legal_moves,
    apply_move,
    is_terminal,
    finalize_if_terminal,
    score,
    winner,
)

@pytest.fixture
def cfg():
    return GameConfig(pits_per_side=6)


def test_init_state_shape_and_values(cfg):
    s = init_state(cfg)
    b = s.board

    assert len(b) == cfg.board_size
    assert s.player == 0
    assert s.config == cfg

    assert b[cfg.p0_store] == 0
    assert b[cfg.p1_store] == 0

    assert all(b[i] == 4 for i in cfg.pits_range(0))
    assert all(b[i] == 4 for i in cfg.pits_range(1))


def test_legal_moves_initial_p0(cfg):
    s = init_state(cfg)
    assert legal_moves(s) == list(cfg.pits_range(0))


def test_apply_move_extra_turn_from_initial_pit2(cfg):
    # With 6 pits/side and 4 stones/pit, pit 2 ends in P0 store => extra turn
    s = init_state(cfg)
    s2, extra = apply_move(s, 2)

    assert extra is True
    assert s2.player == 0

    b = s2.board
    expected = (
        4, 4, 0, 5, 5, 5, 1,  # 0..6 (store at 6)
        4, 4, 4, 4, 4, 4, 0   # 7..13 (store at 13)
    )
    assert b == expected


def test_sowing_skips_opponent_store_capture_can_occur(cfg):
    # This setup causes a capture at the end; still verifies opponent store is not sown into.
    b = [0] * cfg.board_size
    b[5] = 10
    s = GameState(board=tuple(b), player=0, config=cfg)

    s2, _ = apply_move(s, 5)
    b2 = s2.board

    # Opponent store must not receive sown stones (stays 0 here)
    assert b2[cfg.p1_store] == 0

    # In this exact scenario, last stone lands in empty pit 2 and opposite pit 10 has 1 => capture
    assert b2[cfg.p0_store] == 3
    assert b2[2] == 0
    assert b2[10] == 0


def test_capture_rule(cfg):
    # Player 0 plays pit 1 with 1 stone -> lands in pit 2 (empty)
    # opposite pit (10) has stones -> capture into P0 store
    b = [0] * cfg.board_size
    b[1] = 1
    b[10] = 5
    s = GameState(board=tuple(b), player=0, config=cfg)

    s2, extra = apply_move(s, 1)
    assert extra is False

    b2 = s2.board
    assert b2[2] == 0
    assert b2[10] == 0
    assert b2[cfg.p0_store] == 6
    assert s2.player == 1


def test_terminal_sweep_when_one_side_empty(cfg):
    # P0 has one stone in pit 5 -> goes into store -> P0 side empty => terminal => sweep P1 side into P1 store
    b = [0] * cfg.board_size
    b[5] = 1
    b[7] = 2  # P1 side has stones
    s = GameState(board=tuple(b), player=0, config=cfg)

    s2, extra = apply_move(s, 5)
    assert extra is True
    assert is_terminal(s2) is True

    b2 = s2.board
    assert all(b2[i] == 0 for i in cfg.pits_range(0))
    assert all(b2[i] == 0 for i in cfg.pits_range(1))
    assert b2[cfg.p0_store] == 1
    assert b2[cfg.p1_store] == 2


def test_finalize_if_terminal_does_not_change_non_terminal(cfg):
    s = init_state(cfg)
    s2 = finalize_if_terminal(s)
    assert s2 == s


def test_invalid_move_wrong_side(cfg):
    s = init_state(cfg)
    with pytest.raises(ValueError):
        # pick a pit on player 1 side
        apply_move(s, next(iter(cfg.pits_range(1))))


def test_invalid_move_empty_pit(cfg):
    b = list(init_state(cfg).board)
    first_pit = next(iter(cfg.pits_range(0)))
    b[first_pit] = 0
    s = GameState(board=tuple(b), player=0, config=cfg)

    with pytest.raises(ValueError):
        apply_move(s, first_pit)


def test_score_and_winner(cfg):
    # score = P0 store - P1 store
    b = [0] * cfg.board_size
    b[cfg.p0_store] = 10
    b[cfg.p1_store] = 7
    s = GameState(board=tuple(b), player=0, config=cfg)

    assert score(s) == 3
    assert winner(s) == 0

    b[cfg.p0_store] = 5
    b[cfg.p1_store] = 5
    s = GameState(board=tuple(b), player=0, config=cfg)

    assert winner(s) is None