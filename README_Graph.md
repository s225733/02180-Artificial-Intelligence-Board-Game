# graph.py — Alpha-Beta Pruning Visualizer

A standalone visualization tool for the Kalaha minimax agent. Instruments the alpha-beta search and produces two outputs: a static PNG for quick inspection and a zoomable interactive HTML tree for deeper exploration.

## Outputs

| File | Description |
|------|-------------|
| `kalaha_alpha_beta_static.png` | Clean, labeled tree rendered with matplotlib. Readable at low depth. |
| `kalaha_alpha_beta_interactive.html` | Full-depth tree with pan/zoom via Plotly. Open in any browser. |

## Usage

Drop `graph.py` next to `minimax.py` and run:

```bash
python graph.py
```

## Configuration

Edit the constants at the top of the file:

```python
STATIC_DEPTH      = 3   # depth for the PNG (keep low for readability)
INTERACTIVE_DEPTH = 6   # depth for the interactive HTML
STONES_PER_PIT    = 6
PITS_PER_SIDE     = 6
```

## Dependencies

```bash
pip install matplotlib plotly
```

Requires the game package (`game.logic`) to be on the Python path.

## Node Colours

| Colour | Meaning |
|--------|---------|
| Blue   | MAX node (player 0) |
| Purple | MIN node (player 1) |
| Red    | Pruned — never evaluated |

Each node displays its minimax value and the α/β window at the time it was visited. Pruned edges are shown as dashed red lines.

## Output Summary

After each run, the console prints a summary:

```
depth=3 → 142 nodes, 38 pruned, best pit=2
```
```

---

That covers everything a reader needs to run it, configure it, and understand the output at a glance. Let me know if you want it adjusted — e.g. a shorter version, or if you'd like to add a screenshot placeholder.