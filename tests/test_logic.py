import pytest
from game.logic import (
    P0_STORE,
    P1_STORE,
    GameState,
    init_state,
    legal_moves,
    apply_move,
    is_terminal,
    finalize_if_terminal,
    score,
    winner,
)

def test_init_state_shape_and_values():
    s = init_state()
    b = s.board
    assert len(b) == 14
    assert s.player == 0
    assert b[P0_STORE] == 0
    assert b[P1_STORE] == 0
    assert all(b[i] == 4 for i in range(0, 6))
    assert all(b[i] == 4 for i in range(7, 13))


def test_legal_moves_initial_p0():
    s = init_state()
    assert legal_moves(s) == [0, 1, 2, 3, 4, 5]


def test_apply_move_extra_turn_from_initial_pit2():
    # From initial, playing pit 2 (4 stones) lands last stone in P0 store => extra turn
    s = init_state()
    s2, extra = apply_move(s, 2)
    assert extra is True
    assert s2.player == 0  # same player again

    b = s2.board
    expected = (
        4, 4, 0, 5, 5, 5, 1,  # 0..6
        4, 4, 4, 4, 4, 4, 0   # 7..13
    )
    assert b == expected


def test_sowing_skips_opponent_store_even_if_capture_occurs():
    # Force a move that would pass over opponent store (index 13) for player 0.
    # Put 10 stones in pit 5 so sowing goes: 6,7,8,9,10,11,12, (skip 13), 0,1,2
    b = [0] * 14
    b[5] = 10
    b[P0_STORE] = 0
    b[P1_STORE] = 0
    s = GameState(board=tuple(b), player=0)

    s2, _ = apply_move(s, 5)
    b2 = s2.board

    # Opponent store must remain unchanged
    assert b2[P1_STORE] == 0

    # Check key placements
    assert b2[P0_STORE] == 3  # got 3 in own store
    assert b2[7] == 1
    assert b2[12] == 1
    assert b2[10] == 0
    assert b2[2] == 0


def test_capture_rule():
    # Set up: player 0 plays pit 1 with 1 stone, lands in pit 2 (empty),
    # opposite pit (10) has stones => capture into P0 store.
    b = [0] * 14
    b[1] = 1
    b[2] = 0
    b[10] = 5
    b[P0_STORE] = 0
    b[P1_STORE] = 0
    s = GameState(board=tuple(b), player=0)

    s2, extra = apply_move(s, 1)
    assert extra is False
    b2 = s2.board

    assert b2[2] == 0          # landed then captured, so cleared
    assert b2[10] == 0         # opposite cleared
    assert b2[P0_STORE] == 6   # 1 (own) + 5 (opposite)

    # Player should switch (no extra turn)
    assert s2.player == 1


def test_terminal_sweep_when_one_side_empty():
    # Player 0 has a single stone in pit 5; moving it drops into store => extra turn,
    # and then P0 side is empty => terminal => sweep P1 pits into P1 store.
    b = [0] * 14
    b[5] = 1
    b[P0_STORE] = 0
    b[P1_STORE] = 0
    b[7] = 2  # remaining stones on P1 side
    s = GameState(board=tuple(b), player=0)

    s2, extra = apply_move(s, 5)
    assert extra is True  # last stone into store
    assert is_terminal(s2) is True

    b2 = s2.board
    assert all(b2[i] == 0 for i in range(0, 6))
    assert all(b2[i] == 0 for i in range(7, 13))
    assert b2[P0_STORE] == 1
    assert b2[P1_STORE] == 2


def test_finalize_if_terminal_does_not_change_non_terminal():
    s = init_state()
    s2 = finalize_if_terminal(s)
    assert s2 == s


def test_invalid_move_wrong_side():
    s = init_state()
    with pytest.raises(ValueError):
        apply_move(s, 7)  # pit on player 1 side, but it's player 0's turn


def test_invalid_move_empty_pit():
    b = list(init_state().board)
    b[0] = 0
    s = GameState(board=tuple(b), player=0)
    with pytest.raises(ValueError):
        apply_move(s, 0)


def test_score_and_winner():
    # Terminal state where stores decide winner
    b = [0] * 14
    b[P0_STORE] = 10
    b[P1_STORE] = 7
    s = GameState(board=tuple(b), player=0)
    assert score(s) == 3
    assert winner(s) == 0

    b[P0_STORE] = 5
    b[P1_STORE] = 5
    s = GameState(board=tuple(b), player=0)
    assert winner(s) is None