"""
graph.py — Alpha-Beta pruning visualizer for the Kalaha minimax agent.

Produces two outputs:
  1. kalaha_alpha_beta_static.png  — clean static image at low depth (readable)
  2. kalaha_alpha_beta_interactive.html — zoomable/pannable full-depth tree

Drop next to minimax.py and run:  python graph.py
Requires: pip install matplotlib plotly
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
from pathlib import Path
from collections import defaultdict, deque

from game.logic import (
    apply_move,
    init_state,
    is_terminal,
    legal_moves,
    winner,
    GameConfig,
)

# ── Config ────────────────────────────────────────────────────────────────────

STATIC_DEPTH      = 3   # depth for the readable PNG
INTERACTIVE_DEPTH = 6   # depth for the interactive HTML
STONES_PER_PIT    = 6
PITS_PER_SIDE     = 6

# ── Utility ───────────────────────────────────────────────────────────────────

def _score_diff(state):
    return state.board[PITS_PER_SIDE] - state.board[PITS_PER_SIDE * 2 + 1]

def utility_eval(state, player):
    if is_terminal(state):
        w = winner(state)
        if w is None:     return 0
        elif w == player: return 1
        else:             return -1
    diff = _score_diff(state)
    return diff if player == 0 else -diff

def _fmt(v):
    if v ==  np.inf: return "+∞"
    if v == -np.inf: return "-∞"
    return f"{v:+.0f}"

# ── Instrumented search ───────────────────────────────────────────────────────

def run_search(depth):
    """Run alpha-beta search and return (node_meta, edges, best_action)."""
    steps     = []
    edges     = []
    node_meta = {}
    counter   = [0]

    def new_node(state, parent_id, alpha, beta):
        nid = counter[0]
        counter[0] += 1
        node_meta[nid] = dict(
            player = state.player,
            value  = None,
            alpha  = alpha,
            beta   = beta,
            pruned = False,
        )
        if parent_id is not None:
            edges.append((parent_id, nid))
        return nid

    def ab(state, depth, alpha, beta, maximizing_player, parent_id=None):
        nid = new_node(state, parent_id, alpha, beta)

        if is_terminal(state) or depth == 0:
            val = utility_eval(state, maximizing_player)
            node_meta[nid]["value"] = val
            return val

        moves = legal_moves(state)

        if state.player == maximizing_player:
            max_val = -np.inf
            pruned  = []
            for action in moves:
                ns, _ = apply_move(state, action)
                val   = ab(ns, depth-1, alpha, beta, maximizing_player, nid)
                max_val = max(max_val, val)
                alpha   = max(alpha, val)
                if beta <= alpha:
                    for rm in moves[moves.index(action)+1:]:
                        ps, _ = apply_move(state, rm)
                        pnid  = new_node(ps, nid, alpha, beta)
                        node_meta[pnid]["pruned"] = True
                        pruned.append(pnid)
                    break
            node_meta[nid]["value"] = max_val
            return max_val
        else:
            min_val = np.inf
            pruned  = []
            for action in moves:
                ns, _ = apply_move(state, action)
                val   = ab(ns, depth-1, alpha, beta, maximizing_player, nid)
                min_val = min(min_val, val)
                beta    = min(beta, val)
                if beta <= alpha:
                    for rm in moves[moves.index(action)+1:]:
                        ps, _ = apply_move(state, rm)
                        pnid  = new_node(ps, nid, alpha, beta)
                        node_meta[pnid]["pruned"] = True
                        pruned.append(pnid)
                    break
            node_meta[nid]["value"] = min_val
            return min_val

    root_state        = init_state(GameConfig(pits_per_side=PITS_PER_SIDE), stones_per_pit=STONES_PER_PIT)
    maximizing_player = root_state.player
    best_action       = None
    best_value        = -np.inf
    root_id           = new_node(root_state, None, -np.inf, np.inf)

    for action in legal_moves(root_state):
        ns, _ = apply_move(root_state, action)
        val   = ab(ns, depth-1, -np.inf, np.inf, maximizing_player, root_id)
        if val > best_value:
            best_value  = val
            best_action = action

    node_meta[root_id]["value"] = best_value
    n_pruned = sum(1 for m in node_meta.values() if m["pruned"])
    print(f"  depth={depth} → {len(node_meta)} nodes, {n_pruned} pruned, best pit={best_action}")
    return node_meta, edges, best_action

# ── Layout ────────────────────────────────────────────────────────────────────

def compute_layout(edges, node_ids):
    children   = defaultdict(list)
    has_parent = set()
    for p, c in edges:
        children[p].append(c)
        has_parent.add(c)

    roots    = [n for n in node_ids if n not in has_parent] or [min(node_ids)]
    depth_of = {}
    queue    = deque()
    for r in roots:
        depth_of[r] = 0
        queue.append(r)
    while queue:
        n = queue.popleft()
        for c in children[n]:
            if c not in depth_of:
                depth_of[c] = depth_of[n] + 1
                queue.append(c)

    by_depth  = defaultdict(list)
    for n, d in depth_of.items():
        by_depth[d].append(n)

    pos       = {}
    max_width = max(len(v) for v in by_depth.values())
    for d, nodes in by_depth.items():
        nodes = sorted(nodes)
        n     = len(nodes)
        for i, node in enumerate(nodes):
            x = (i - (n-1)/2) * (max_width / max(n, 1)) * 1.6
            y = -d * 1.8
            pos[node] = (x, y)
    return pos

# ── Static PNG (matplotlib) ───────────────────────────────────────────────────

def render_static(node_meta, edges, best_action, depth):
    PALETTE = {
        "bg":     "#0d1117",
        "max":    "#1a3a6a",
        "min":    "#3a1a6a",
        "pruned": "#6a1a1a",
        "edge":   "#334455",
        "pedge":  "#883333",
    }

    node_ids   = list(node_meta.keys())
    pos        = compute_layout(edges, node_ids)
    pruned_set = {nid for nid, m in node_meta.items() if m["pruned"]}
    n_pruned   = len(pruned_set)
    n_eval     = len(node_ids) - n_pruned

    fig, ax = plt.subplots(figsize=(28, 16))
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])
    ax.axis("off")

    for p, c in edges:
        if p not in pos or c not in pos: continue
        x0, y0 = pos[p]; x1, y1 = pos[c]
        color = PALETTE["pedge"] if c in pruned_set else PALETTE["edge"]
        ax.plot([x0, x1], [y0, y1], color=color, lw=1.0,
                ls="--" if c in pruned_set else "-", zorder=1)

    for nid in node_ids:
        if nid not in pos: continue
        x, y = pos[nid]
        meta = node_meta[nid]
        r    = 0.45
        fc   = PALETTE["pruned"] if meta["pruned"] else (PALETTE["max"] if meta["player"] == 0 else PALETTE["min"])

        ax.add_patch(plt.Circle((x, y), r, color=fc, zorder=3, ec="#ffffff15", lw=1))

        val_str = _fmt(meta["value"]) if meta["value"] is not None else "?"
        ax.text(x, y + 0.10, val_str, ha="center", va="center",
                fontsize=7.5, color="white", fontweight="bold", zorder=4)
        ax.text(x, y - r - 0.18,
                f"α={_fmt(meta['alpha'])}  β={_fmt(meta['beta'])}",
                ha="center", va="top", fontsize=5, color="#9999bb", zorder=4)
        if not meta["pruned"]:
            ax.text(x, y + r + 0.12,
                    "MAX" if meta["player"] == 0 else "MIN",
                    ha="center", va="bottom", fontsize=5.5, color="#ccccaa", zorder=4)

    ax.set_title(
        f"Kalaha Minimax · Alpha-Beta Pruning  |  depth={depth}  |  best action → pit {best_action}\n"
        f"Nodes evaluated: {n_eval}   Nodes pruned: {n_pruned}   Total: {len(node_ids)}",
        color="white", fontsize=11, pad=14,
    )
    ax.legend(handles=[
        mpatches.Patch(color=PALETTE["max"],    label="MAX node (player 0)"),
        mpatches.Patch(color=PALETTE["min"],    label="MIN node (player 1)"),
        mpatches.Patch(color=PALETTE["pruned"], label="Pruned — never evaluated"),
    ], loc="lower right", fontsize=8, facecolor="#1a1d2e",
       edgecolor="#333355", labelcolor="white", framealpha=0.9)

    out = Path(__file__).parent / "kalaha_alpha_beta_static.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print(f"  Static PNG → {out}")

# ── Interactive HTML (plotly) ─────────────────────────────────────────────────

def render_interactive(node_meta, edges, best_action, depth):
    node_ids   = list(node_meta.keys())
    pos        = compute_layout(edges, node_ids)
    pruned_set = {nid for nid, m in node_meta.items() if m["pruned"]}
    n_pruned   = len(pruned_set)
    n_eval     = len(node_ids) - n_pruned

    # Edge traces — split normal vs pruned for separate styling
    ex_norm, ey_norm = [], []
    ex_prune, ey_prune = [], []
    for p, c in edges:
        if p not in pos or c not in pos: continue
        x0, y0 = pos[p]; x1, y1 = pos[c]
        if c in pruned_set:
            ex_prune += [x0, x1, None]; ey_prune += [y0, y1, None]
        else:
            ex_norm  += [x0, x1, None]; ey_norm  += [y0, y1, None]

    traces = [
        go.Scatter(x=ex_norm,  y=ey_norm,  mode="lines",
                   line=dict(color="#334455", width=1),
                   hoverinfo="none", showlegend=False),
        go.Scatter(x=ex_prune, y=ey_prune, mode="lines",
                   line=dict(color="#883333", width=1, dash="dash"),
                   hoverinfo="none", showlegend=False),
    ]

    # Node traces — one per category
    categories = {
        "MAX (player 0)": ("#1a3a6a", []),
        "MIN (player 1)": ("#3a1a6a", []),
        "Pruned":         ("#6a1a1a", []),
    }

    for nid in node_ids:
        if nid not in pos: continue
        x, y = pos[nid]
        meta = node_meta[nid]
        val_str = _fmt(meta["value"]) if meta["value"] is not None else "?"
        tip = (f"Node {nid}<br>"
               f"Player: {meta['player']}<br>"
               f"Value: {val_str}<br>"
               f"α={_fmt(meta['alpha'])}  β={_fmt(meta['beta'])}<br>"
               f"{'⚠ PRUNED' if meta['pruned'] else ''}")

        if meta["pruned"]:
            key = "Pruned"
        elif meta["player"] == 0:
            key = "MAX (player 0)"
        else:
            key = "MIN (player 1)"

        categories[key][1].append((x, y, val_str, tip))

    for label, (color, points) in categories.items():
        if not points: continue
        xs, ys, texts, tips = zip(*points)
        traces.append(go.Scatter(
            x=xs, y=ys, mode="markers+text",
            marker=dict(size=18, color=color, line=dict(color="rgba(255,255,255,0.13)", width=1)),
            text=texts, textfont=dict(color="white", size=8),
            textposition="middle center",
            hovertext=tips, hoverinfo="text",
            name=label,
        ))

    fig = go.Figure(traces)
    fig.update_layout(
        title=dict(
            text=(f"Kalaha Minimax · Alpha-Beta Pruning  |  depth={depth}  |  best action → pit {best_action}<br>"
                  f"<sup>Nodes evaluated: {n_eval}   Pruned: {n_pruned}   Total: {len(node_ids)}</sup>"),
            font=dict(color="white", size=13),
        ),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="white"),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        legend=dict(bgcolor="#1a1d2e", bordercolor="#333355", borderwidth=1),
        hovermode="closest",
        height=850,
    )

    out = Path(__file__).parent / "kalaha_alpha_beta_interactive.html"
    fig.write_html(str(out))
    print(f"  Interactive HTML → {out}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Running static search  (depth={STATIC_DEPTH})...")
    nm_s, ed_s, best_s = run_search(STATIC_DEPTH)
    render_static(nm_s, ed_s, best_s, STATIC_DEPTH)

    print(f"Running interactive search (depth={INTERACTIVE_DEPTH})...")
    nm_i, ed_i, best_i = run_search(INTERACTIVE_DEPTH)
    render_interactive(nm_i, ed_i, best_i, INTERACTIVE_DEPTH)

    print("Done.")