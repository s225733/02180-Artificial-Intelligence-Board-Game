# Full Game Performance Experiment

## Purpose

This experiment measures the practical runtime and memory usage of the Kalaha AI implementation during a full game.

The AI uses the Minimax algorithm with Alpha-Beta pruning to choose actions. The experiment simulates complete AI-vs-AI games and measures:

- Total runtime required to finish a full game
- Peak RAM usage during execution

The goal is to evaluate the practical time and space requirements of the algorithm for a given search depth.

## What the Experiment Does

The experiment runs several full Kalaha games where both players use the same AI agent.

For each game run:

1. The board is initialized with 6 stones per pit.
2. The game proceeds until a terminal state is reached.
3. Each move is selected using: `choose_action(state, depth)`, which performs a Minimax search with Alpha-Beta pruning.

During the execution of the full game, the following metrics are measured:

- Elapsed time
- Peak RAM usage
- Number of moves played
- Winner of the game

The experiment is repeated multiple times to obtain stable performance measurements.

## Interpretation of Results

The experiment provides an empirical estimate of the algorithm's performance.

From the example results:

- A full AI-vs-AI Kalaha game at search depth 5 takes approximately 0.34 seconds on average.
- Peak RAM usage is approximately 25 MB.
- Runtime variation across runs is small, indicating stable performance.

These results suggest that the implementation is computationally efficient for the tested search depth.

## Deterministic Results

The AI algorithm is deterministic, meaning:

- The same starting board produces the same sequence of moves.
- The number of moves and the winner remain the same across runs.

This is expected and helps produce consistent performance measurements.
