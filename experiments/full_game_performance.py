"""Experiment for measuring runtime and peak RAM over multiple full AI-vs-AI games."""

from __future__ import annotations

from statistics import mean

from ai_agent.minimax import choose_action
from game.config import GameConfig
from game.logic import apply_move, init_state, is_terminal, winner
from utils.measure_utils import measure_time_and_peak_ram


def play_full_game(depth: int = 7) -> dict[str, int | None]:
    """
    Simulate one full AI-vs-AI game with the same depth. 

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
    depths = list(range(1, 11))  # depth from 1 to 10
    runs = 10

    all_results = []

    for depth in depths:
        elapsed_times = []
        peak_rams = []
        move_counts = []
        winners = []

        for run_number in range(1, runs + 1):
            metrics = measure_time_and_peak_ram(play_full_game, depth=depth)
            result = metrics["result"]

            elapsed_times.append(metrics["elapsed_seconds"])
            peak_rams.append(metrics["peak_ram_mb"])
            move_counts.append(result["move_count"])
            winners.append(result["winner"])

            # stops runs for that depth
            if metrics["elapsed_seconds"] > 6:
                print(f"Stopping early at depth {depth} and at run number {run_number} because it is too slow")
                break

        
        p0_wins = sum(1 for w in winners if w == 0)
        p1_wins = sum(1 for w in winners if w == 1)
        draws = sum(1 for w in winners if w is None)

        summary = {
            "depth": depth,
            "runs": len(elapsed_times),  
            "avg_time": mean(elapsed_times), 
            "fastest_time": min(elapsed_times), 
            "slowest_time": max(elapsed_times),
            "avg_moves": mean(move_counts), 
            "min_moves": min(move_counts), 
            "max_moves": max(move_counts),
            "avg_ram": mean(peak_rams), 
            "max_ram": max(peak_rams),  
            "min_ram": min(peak_rams), 
            "p0_wins": p0_wins,
            "p1_wins": p1_wins,
            "draws": draws,
        }

        all_results.append(summary)

        # stops all further depths
        if summary["slowest_time"] and summary["slowest_time"] > 6:
            print(f"Stopping depth search at {depth} because it run time takes too long")
            break


   
    print("\n=== RESULTS TABLE ===")
    print("Depth  |   Avg time |   Max time |    Avg RAM |    Max RAM |  Avg moves")
    print("-" * 76)
    for r in all_results:
        print(
            f"{r['depth']:<6} | "
            f"{r['avg_time']:>10.6f} | "
            f"{r['slowest_time']:>10.6f} | "
            f"{r['avg_ram']:>10.3f} | "
            f"{r['max_ram']:>10.3f} | "
            f"{r['avg_moves']:>10.2f}"
        )

    print("\n=== FULL SUMMARY BY DEPTH ===")
    for r in all_results:
        print(f"\nDepth {r['depth']}")
        print(f"Number of runs: {r['runs']}")
        print(f"Average time: {r['avg_time']:.6f} s")
        print(f"Fastest time: {r['fastest_time']:.6f} s")
        print(f"Slowest time: {r['slowest_time']:.6f} s")
        print(f"Average moves played: {r['avg_moves']:.2f}")
        print(f"Min moves played: {r['min_moves']}")
        print(f"Max moves played: {r['max_moves']}")
        print(f"Average peak RAM: {r['avg_ram']:.3f} MB")
        print(f"Highest observed peak RAM: {r['max_ram']:.3f} MB")
        print(f"Lowest observed peak RAM: {r['min_ram']:.3f} MB")
        print(f"Player 0 wins: {r['p0_wins']}")
        print(f"Player 1 wins: {r['p1_wins']}")
        print(f"Draws: {r['draws']}")

if __name__ == "__main__":
    main()