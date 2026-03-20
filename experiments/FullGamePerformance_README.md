# Full Game Performance Experiment

## Purpose

This experiment measures the practical runtime and memory usage of the Kalaha AI during a full game. 

Two experiments conducted:
1. A depth comparison experiment evaluating different depth strength and weaknesses `(depth_comparison)`
2. A perfomance experiment measuring run time and memory usage `(full_game_performance)`

The goal is to evaluate the practical time and space requirements of the algorithm for a given search depth and by comparing the results we can find an optimal depth. 

## What the Depth Comparison Experiment Does: 
The experiment is conducted to compare the playing strength of different search depths.

For each comparison:
- One player ues depth a
- The other uses depth b
- The match is plaued multipled times with swapped depth and starting positions

Once they are compared the following metrics is used to measure:
- Number of wins for each depth
- Number of draws
- Scoring rate for each depth
- Average time per game 

The experiments helps determine whether deeper search provides a meaningful advantage in the game. 

## What the Full Game Perfomance Experiment Does

This experiment measures the computational cost of the AI. It runs several full Kalaha games where both players use:
- Use the same depth
- Depth varys from 1-10

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

By combining both experiments an optimal depth is evaluted to be 7. 

The results shows that:

- A full AI-vs-AI Kalaha game at search depth 7 takes approximately 0.6 seconds on average with a run on 10 times.
- Peak RAM usage is approximately 25 MB.
- Runtime variation across runs is small, indicating stable performance.

These results suggest that the implementation is computationally efficient for the tested search depth.

## Deterministic Results

The AI algorithm is deterministic, meaning:

- The same starting board produces the same sequence of moves.
- The number of moves and the winner remain the same across runs.

This is expected and helps produce consistent performance measurements.