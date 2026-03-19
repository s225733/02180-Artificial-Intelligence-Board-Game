# Full Game Performance Experiment

## Purpose

This experiment measures the practical runtime and memory usage of the Kalaha AI during a full game. To evaluate how performance scales, the experiment is repeated for multiple search depths from 1 to 10, allowing comparison of computational cost across increasing levels of search complexity.

The AI uses the Minimax algorithm with Alpha-Beta pruning to choose actions. The experiment simulates complete AI-vs-AI games and measures:

- Total runtime required to finish a full game
- Peak RAM usage during execution

The goal is to evaluate the practical time and space requirements of the algorithm for a given search depth.

## What the Experiment Does

The experiment runs several full Kalaha games where both players use the same AI agent. During the experiment multiple full games are simulated with different search depth to evaluate the perfomance metrics.

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

## Additional Experiment: Depth Comparison

In addition to the full game perfomance experiment, a separate experiment is conducted to compare the playing strength of different search depth.

While the full game perfomance experiment evaluated computational cost when both players have the same depth, "Depth Comparison" compare two different depths. This is implemented to help evaluate which depth is better in terms of win rate and the perfomance metrics. By comparing search depth we can see if an increase in depths leads to a meaningful improvent in perfomance or not. 

For each comparison:
- player 1 have one depth
- player 2 have another depth
- The game is played multiple times with swapped starting state and action to reduce any biases 


The experiments measures:
- Number of wins for each of the depth
- Number of draws
- Score rate of the depths
- Average time per game 