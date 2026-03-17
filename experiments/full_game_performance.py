"""Experiment for measuring runtime and peak RAM over multiple full AI-vs-AI games."""

from __future__ import annotations

from statistics import mean

from ai_agent.minimax import choose_action
from game.config import GameConfig
from game.logic import apply_move, init_state, is_terminal, winner
from utils.measure_utils import measure_time_and_peak_ram


def play_full_game(depth: int = 5) -> dict[str, int | None]:
    """
    Simulate one full AI-vs-AI game.

    Returns a dictionary containing:
    - winner
    - move_count
    """
    cfg = GameConfig(pits_per_side=6)
    state = init_state(cfg, stones_per_pit=6)
    move_count = 0

    while not is_terminal(state):
        move = choose_action(state, depth=depth)
        state, _ = apply_move(state, move)
        move_count += 1

    return {
        "winner": winner(state),
        "move_count": move_count,
    }


def main() -> None:
    depth = 5
    runs = 10

    elapsed_times: list[float] = []
    peak_rams: list[float] = []
    move_counts: list[int] = []
    winners: list[int | None] = []

    for run_number in range(1, runs + 1):
        metrics = measure_time_and_peak_ram(play_full_game, depth=depth)
        result = metrics["result"]

        elapsed_times.append(metrics["elapsed_seconds"])
        peak_rams.append(metrics["peak_ram_mb"])
        move_counts.append(result["move_count"])
        winners.append(result["winner"])

        print(
            f"Run {run_number:02d} | "
            f"time={metrics['elapsed_seconds']:.6f} s | "
            f"peak_ram={metrics['peak_ram_mb']:.3f} MB | "
            f"moves={result['move_count']} | "
            f"winner={result['winner']}"
        )

    print("\n=== Summary ===")
    print(f"Search depth: {depth}")
    print(f"Number of runs: {runs}")

    print(f"Average time: {mean(elapsed_times):.6f} s")
    print(f"Fastest time: {min(elapsed_times):.6f} s")
    print(f"Slowest time: {max(elapsed_times):.6f} s")

    print(f"Average moves played: {mean(move_counts):.2f}")
    print(f"Min moves played: {min(move_counts)}")
    print(f"Max moves played: {max(move_counts)}")

    print(f"Average peak RAM: {mean(peak_rams):.3f} MB")
    print(f"Highest observed peak RAM: {max(peak_rams):.3f} MB")
    print(f"Lowest observed peak RAM: {min(peak_rams):.3f} MB")

    p0_wins = sum(1 for w in winners if w == 0)
    p1_wins = sum(1 for w in winners if w == 1)
    draws = sum(1 for w in winners if w is None)

    print(f"Player 0 wins: {p0_wins}")
    print(f"Player 1 wins: {p1_wins}")
    print(f"Draws: {draws}")


if __name__ == "__main__":
    main()