from __future__ import annotations

from statistics import mean

from ai_agent.minimax import choose_action
from game.config import GameConfig
from game.logic import apply_move, init_state, is_terminal, winner
from utils.measure_utils import measure_time_and_peak_ram


def play_match(depth_p0: int, depth_p1: int) -> dict[str, int | None]:
    """
    Simulate one full AI-vs-AI game where player 0 and player 1
    can use different search depths.
    """
    cfg = GameConfig(pits_per_side=6)
    state = init_state(cfg, stones_per_pit=6)
    move_count = 0

    while not is_terminal(state):
        if state.player == 0:
            move = choose_action(state, depth=depth_p0)
        else:
            move = choose_action(state, depth=depth_p1)

        state, _ = apply_move(state, move)
        move_count += 1

    return {
        "winner": winner(state),
        "move_count": move_count,
    }


def compare_depths(depth_a: int, depth_b: int, runs: int) -> None:
    """

    Run matches in both directions:
    - depth_a as player 0 vs depth_b as player 1
    - depth_b as player 0 vs depth_a as player 1

    """
    elapsed_times: list[float] = []
    peak_rams: list[float] = []
    move_counts: list[int] = []

    depth_a_wins = 0
    depth_b_wins = 0
    draws = 0

    # First half: A as player 0, B as player 1
    for _ in range(runs):
        metrics = measure_time_and_peak_ram(play_match, depth_p0=depth_a, depth_p1=depth_b)
        result = metrics["result"]

        elapsed_times.append(metrics["elapsed_seconds"])
        peak_rams.append(metrics["peak_ram_mb"])
        move_counts.append(result["move_count"])

        if result["winner"] == 0:
            depth_a_wins += 1
        elif result["winner"] == 1:
            depth_b_wins += 1
        else:
            draws += 1

    # Second half: B as player 0, A as player 1
    for _ in range(runs):
        metrics = measure_time_and_peak_ram(play_match, depth_p0=depth_b, depth_p1=depth_a)
        result = metrics["result"]

        elapsed_times.append(metrics["elapsed_seconds"])
        peak_rams.append(metrics["peak_ram_mb"])
        move_counts.append(result["move_count"])

        if result["winner"] == 0:
            depth_b_wins += 1
        elif result["winner"] == 1:
            depth_a_wins += 1
        else:
            draws += 1

    total_games = 2 * runs

    # calculating the score rate for each of the depths
    depth_a_score_rate = (depth_a_wins + (0.5 * draws)) / total_games
    depth_b_score_rate = (depth_b_wins + (0.5 * draws)) / total_games

    print(f"\n=== Depth {depth_a} vs Depth {depth_b} ===")
    print(f"Total games: {total_games}")
    print(f"Depth {depth_a} wins: {depth_a_wins}")
    print(f"Depth {depth_b} wins: {depth_b_wins}")
    print(f"Draws: {draws}")
    print(f"Depth {depth_a} score rate: {depth_a_score_rate:.2%}")
    print(f"Depth {depth_b} score rate: {depth_b_score_rate:.2%}")
    print(f"Average time per game: {mean(elapsed_times):.6f} s")
    print(f"Max time per game: {max(elapsed_times):.6f} s")
    print(f"Average peak RAM: {mean(peak_rams):.3f} MB")
    print(f"Highest peak RAM: {max(peak_rams):.3f} MB")


def main() -> None:
    runs = 10

    compare_depths(depth_a=7, depth_b=8, runs=runs)
    compare_depths(depth_a=7, depth_b=6, runs=runs)
    compare_depths(depth_a=7, depth_b=5, runs=runs)


if __name__ == "__main__":
    main()