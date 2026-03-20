# 02180-Artificial-Intelligence-Board-Game

This is for the course 02180 and has the focus of creating GOFAI for a board game.

## Installation

### Clone the repository

```bash
git clone https://github.com/s225733/02180-Artificial-Intelligence-Board-Game.git
cd 02180-Artificial-Intelligence-Board-Game
```

### Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Run experiments

When running the experiments, please be patient and avoid interrupting execution.
The runtime grows exponentially with the search depth due to the branching factor of the game tree.
Depths up to 8 remain computationally manageable, while depths ≥ 9 may result in significantly longer execution times due to complexity of $O(b^d)$

To run experiments, you run the following command from root directory:


For full game perfomance run:

```bash
python3 -m experiments.full_game_performance
```

For depth comparison run:
```bash
python3 -m experiments.depth_comparison
```


