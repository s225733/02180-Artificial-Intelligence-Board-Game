"""Command-line interface for Kalaha.

This file allows the game to be played in the terminal using text-based input.
It uses the core game logic from the game package.
"""

from game.config import GameConfig
from game.logic import (
    GameState, init_state, legal_moves, apply_move, is_terminal, winner
)



def render(state: GameState) -> str:
    """Return a text representation of the current board."""
    b = state.board
    cfg = state.config

    # Top row: P1 pits right-to-left
    top = "  " + " ".join(
        f"{b[i]:2d}" for i in range(2 * cfg.pits_per_side, cfg.pits_per_side, -1)
    )

    # Stores
    mid = f"{b[cfg.p1_store]:2d} " + " " * (3 * cfg.pits_per_side + 2) + f"{b[cfg.p0_store]:2d}"

    # Bottom row: P0 pits left-to-right
    bot = "  " + " ".join(f"{b[i]:2d}" for i in range(0, cfg.pits_per_side))

    turn = f"Turn: P{state.player}"
    return "\n".join([turn, top, mid, bot])


def ask_human_move(state: GameState) -> int:
    """Ask the current player to choose a legal move."""
    moves = legal_moves(state)
    print(f"Legal moves: {moves}")
    
    while True:
        raw = input(f"P{state.player} choose pit index: ").strip()
        
        try:
            pit = int(raw)
            if pit in moves:
                return pit
        except ValueError:
            pass
        
        print("Invalid move. Try again.")


def run_cli():
    """Run the text-based Kalaha game."""
    cfg = GameConfig(pits_per_side=6) # You can adjust the amount of pits per side here
    state = init_state(cfg, stones_per_pit=3) # You can adjust the amount of stones per pit here

    while True:
        print()
        print(render(state))

        if is_terminal(state):
            w = winner(state)
            if w is None:
                print("Game over: tie.")
            else:
                print(f"Game over: P{w} wins.")
            break

        pit = ask_human_move(state)
        state, extra = apply_move(state, pit)
        
        if extra:
            print("Extra turn!")


if __name__ == "__main__":
    run_cli()