from logic import (
    GameState, init_state, legal_moves, apply_move, is_terminal, winner
)

P0_STORE = 6
P1_STORE = 13


def render(state: GameState) -> str:
    b = state.board
    top = "  " + " ".join(f"{b[i]:2d}" for i in range(12, 6, -1))
    mid = f"{b[P1_STORE]:2d}                   {b[P0_STORE]:2d}"
    bot = "  " + " ".join(f"{b[i]:2d}" for i in range(0, 6))
    turn = f"Turn: P{state.player}"
    return "\n".join([turn, top, mid, bot])


def ask_human_move(state: GameState) -> int:
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


def main():
    state = init_state()
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
    main()