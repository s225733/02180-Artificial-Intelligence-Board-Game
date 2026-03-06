"""Tkinter user interface for Kalaha."""

from random import Random
from tkinter import Canvas, Label, Tk

from game.config import GameConfig
from game.logic import (
    apply_move,
    init_state,
    is_terminal,
    legal_moves,
    winner,
)
from ai_agent.minimax import choose_action


# ------------------ COLORS ------------------

WINDOW_BG = "#d9c3a0"
CANVAS_BG = "#c9a57a"
BOARD_SHADOW = "#6d4428"
BOARD_OUTER = "#7b4f2c"
BOARD_INNER = "#9a6633"

STORE_FILL = "#6e3f1f"
STORE_OUTLINE = "#3f2413"

TOP_PIT_FILL = "#5a3426"
BOTTOM_PIT_FILL = "#78431f"
PIT_OUTLINE = "#342015"

TEXT_DARK = "#2b1b12"
TEXT_LIGHT = "#f8f1df"

STONE_COLORS = [
    ("#f5e7c7", "#d9c29a"),
    ("#ead7ae", "#cbb080"),
    ("#f0debb", "#d6bf98"),
]


# ------------------ GLOBAL STATE ------------------

cfg = None
state = None
win = None
c = None

left_score = None
right_score = None
status_label = None
subtitle_label = None

top_pits = {}
bottom_pits = {}
top_bounds = {}
bottom_bounds = {}

is_animating = False


# ------------------ SETUP ------------------


def init_game() -> None:
    """Initialize the game configuration and starting state."""
    global cfg, state
    cfg = GameConfig(pits_per_side=6)
    state = init_state(cfg, stones_per_pit=6)


def create_window() -> None:
    """Create the main Tkinter window and canvas."""
    global win, c

    win = Tk()
    win.title("Kalaha")
    win.geometry("980x560")
    win.configure(bg=WINDOW_BG)

    c = Canvas(win, width=980, height=470, bg=CANVAS_BG, highlightthickness=0)
    c.pack(pady=16)

    # Board shadow
    c.create_rectangle(
        76, 76, 906, 386,
        fill=BOARD_SHADOW,
        outline="",
    )

    # Board frame
    c.create_rectangle(
        70, 70, 900, 380,
        fill=BOARD_OUTER,
        outline="#5a341d",
        width=4,
    )

    # Board inner
    c.create_rectangle(
        88, 88, 882, 362,
        fill=BOARD_INNER,
        outline="#a87442",
        width=2,
    )

    # Title
    c.create_text(
        490,
        36,
        text="Kalaha",
        font=("Georgia", 28, "bold"),
        fill=TEXT_DARK,
    )


def create_stores() -> None:
    """Draw the stores and create their score labels."""
    global left_score, right_score

    # Shadows
    c.create_oval(114, 116, 192, 334, fill="#4f2a14", outline="")
    c.create_oval(788, 116, 866, 334, fill="#4f2a14", outline="")

    # Main stores
    c.create_oval(
        108, 110, 186, 328,
        fill=STORE_FILL,
        outline=STORE_OUTLINE,
        width=3,
    )
    c.create_oval(
        782, 110, 860, 328,
        fill=STORE_FILL,
        outline=STORE_OUTLINE,
        width=3,
    )

    # Soft inner highlight
    c.create_oval(
        116, 118, 178, 190,
        outline="",
    )
    c.create_oval(
        790, 118, 852, 190,
        outline="",
    )

    left_score = Label(
        win,
        text="0",
        font=("Helvetica", 20, "bold"),
        bg="#d8b989",
        fg=TEXT_DARK,
        padx=8,
        pady=2,
        relief="flat",
    )
    left_score.place(x=128, y=214)

    right_score = Label(
        win,
        text="0",
        font=("Helvetica", 20, "bold"),
        bg="#d8b989",
        fg=TEXT_DARK,
        padx=8,
        pady=2,
        relief="flat",
    )
    right_score.place(x=802, y=214)


def create_pits() -> None:
    """Draw the top and bottom pits and save their bounds."""
    global top_pits, bottom_pits, top_bounds, bottom_bounds

    pit_width = 90
    pit_height = 90
    start_x = 220
    spacing = 94

    top_pits = {}
    bottom_pits = {}
    top_bounds = {}
    bottom_bounds = {}

    for i in range(cfg.pits_per_side):
        x0 = start_x + i * spacing
        y_top = 120
        y_bottom = 250

        top_bounds[i] = (x0, y_top, x0 + pit_width, y_top + pit_height)
        bottom_bounds[i] = (x0, y_bottom, x0 + pit_width, y_bottom + pit_height)

        # Top row shadows
        c.create_oval(
            x0 + 4, y_top + 5, x0 + pit_width + 4, y_top + pit_height + 5,
            fill="#4a2b1f",
            outline="",
        )

        # Bottom row shadows
        c.create_oval(
            x0 + 4, y_bottom + 5, x0 + pit_width + 4, y_bottom + pit_height + 5,
            fill="#5a3317",
            outline="",
        )

        # Top row pits
        top_pit = c.create_oval(
            x0,
            y_top,
            x0 + pit_width,
            y_top + pit_height,
            fill=TOP_PIT_FILL,
            outline=PIT_OUTLINE,
            width=3,
            tags=(f"top_{i}",),
        )
        top_pits[i] = top_pit

        c.create_oval(
            x0 + 8,
            y_top + 8,
            x0 + pit_width - 10,
            y_top + 34,
            fill="#704738",
            outline="",
        )

        # Bottom row pits
        bottom_pit = c.create_oval(
            x0,
            y_bottom,
            x0 + pit_width,
            y_bottom + pit_height,
            fill=BOTTOM_PIT_FILL,
            outline=PIT_OUTLINE,
            width=3,
            tags=(f"bottom_{i}",),
        )
        bottom_pits[i] = bottom_pit

        c.create_oval(
            x0 + 8,
            y_bottom + 8,
            x0 + pit_width - 10,
            y_bottom + 34,
            fill="#98633e",
            outline="",
        )


def create_player_labels() -> None:
    """Create the player labels."""
    c.create_text(
        490,
        103,
        text="AI",
        font=("Helvetica", 14, "bold"),
        fill=TEXT_LIGHT,
    )
    c.create_text(
        490,
        357,
        text="You",
        font=("Helvetica", 14, "bold"),
        fill=TEXT_LIGHT,
    )


def create_status_label() -> None:
    """Create labels showing turn and mode."""
    global status_label, subtitle_label

    subtitle_label = Label(
        win,
        text="You are Player 1 • AI is Player 2",
        font=("Helvetica", 11),
        bg=WINDOW_BG,
        fg=TEXT_DARK,
    )
    subtitle_label.place(x=382, y=486)

    status_label = Label(
        win,
        text="",
        font=("Helvetica", 14, "bold"),
        bg="#f0dfbf",
        fg=TEXT_DARK,
        padx=14,
        pady=6,
        relief="flat",
    )
    status_label.place(x=420, y=515)


# ------------------ STATUS ------------------


def update_status(message: str | None = None) -> None:
    """Update the status label."""
    if message is not None:
        status_label.config(text=message)
        return

    if is_terminal(state):
        w = winner(state)
        if w is None:
            status_label.config(text="Game over • Draw")
        elif w == 0:
            status_label.config(text="Game over • You win")
        else:
            status_label.config(text="Game over • AI wins")
        return

    if state.player == 0:
        status_label.config(text="Your turn")
    else:
        status_label.config(text="AI's turn")


# ------------------ STONES ------------------


def get_stone_layout(bounds: tuple[float, float, float, float], count: int) -> list[tuple[float, float, float]]:
    """Return deterministic pebble positions inside a pit."""
    if count <= 0:
        return []

    x0, y0, x1, y1 = bounds
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    pit_w = x1 - x0
    pit_h = y1 - y0

    base_radius = min(pit_w, pit_h) * 0.09
    ring_r_x = pit_w * 0.23
    ring_r_y = pit_h * 0.23

    positions = []
    rng = Random((int(x0) * 1000) + (int(y0) * 10) + count)

    # Center-first layout
    slots = [(cx, cy)]

    ring_1 = [
        (cx - ring_r_x, cy),
        (cx + ring_r_x, cy),
        (cx, cy - ring_r_y),
        (cx, cy + ring_r_y),
        (cx - ring_r_x * 0.72, cy - ring_r_y * 0.72),
        (cx + ring_r_x * 0.72, cy - ring_r_y * 0.72),
        (cx - ring_r_x * 0.72, cy + ring_r_y * 0.72),
        (cx + ring_r_x * 0.72, cy + ring_r_y * 0.72),
    ]

    ring_2 = [
        (cx - ring_r_x * 1.25, cy - ring_r_y * 0.15),
        (cx + ring_r_x * 1.25, cy - ring_r_y * 0.15),
        (cx - ring_r_x * 0.15, cy - ring_r_y * 1.18),
        (cx + ring_r_x * 0.15, cy - ring_r_y * 1.18),
        (cx - ring_r_x * 1.0, cy + ring_r_y * 0.95),
        (cx + ring_r_x * 1.0, cy + ring_r_y * 0.95),
    ]

    slots.extend(ring_1)
    slots.extend(ring_2)

    for i in range(min(count, len(slots))):
        sx, sy = slots[i]
        jitter_x = rng.uniform(-2.0, 2.0)
        jitter_y = rng.uniform(-2.0, 2.0)
        radius = base_radius + rng.uniform(-1.2, 1.2)
        positions.append((sx + jitter_x, sy + jitter_y, radius))

    return positions


def draw_stones(bounds: tuple[float, float, float, float], count: int, stone_tag: str, pit_tag: str) -> None:
    """Draw pebbles inside a pit."""
    c.delete(stone_tag)

    for idx, (cx, cy, r) in enumerate(get_stone_layout(bounds, count)):
        fill, outline = STONE_COLORS[idx % len(STONE_COLORS)]

        # shadow
        c.create_oval(
            cx - r + 1.5,
            cy - r + 2,
            cx + r + 1.5,
            cy + r + 2,
            fill="#6f573f",
            outline="",
            tags=(stone_tag, pit_tag),
        )

        # stone
        c.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            fill=fill,
            outline=outline,
            width=1,
            tags=(stone_tag, pit_tag),
        )


def render_board(board: tuple[int, ...] | list[int]) -> None:
    """Render stones in pits and numbers in stores."""
    for i in range(cfg.pits_per_side):
        draw_stones(
            bottom_bounds[i],
            board[i],
            stone_tag=f"bottom_stones_{i}",
            pit_tag=f"bottom_{i}",
        )

    start = cfg.pits_per_side + 1
    end = start + cfg.pits_per_side

    for i in range(cfg.pits_per_side):
        board_index = end - 1 - i
        draw_stones(
            top_bounds[i],
            board[board_index],
            stone_tag=f"top_stones_{i}",
            pit_tag=f"top_{i}",
        )

    left_score.config(text=str(board[cfg.p1_store]))
    right_score.config(text=str(board[cfg.p0_store]))


def render_ui() -> None:
    """Render the current state and update the turn/game status."""
    render_board(state.board)
    update_status()


# ------------------ ANIMATION ------------------


def animate_move(pit_index: int, after_done=None) -> None:
    """Animate sowing stones across the board."""
    global is_animating

    if is_animating:
        return

    mover = state.player
    temp_board = list(state.board)
    stones = temp_board[pit_index]

    if stones <= 0:
        return

    is_animating = True
    temp_board[pit_index] = 0
    render_board(temp_board)

    opp_store = cfg.opponent_store(mover)
    idx = pit_index
    path = []

    while stones > 0:
        idx = (idx + 1) % cfg.board_size
        if idx == opp_store:
            continue
        path.append(idx)
        stones -= 1

    total_animation_ms = 180
    interval = max(14, int(total_animation_ms / max(1, len(path))))

    def step(pos: int = 0) -> None:
        global state, is_animating

        if pos < len(path):
            temp_board[path[pos]] += 1
            render_board(temp_board)
            win.after(interval, lambda: step(pos + 1))
            return

        state, _ = apply_move(state, pit_index)
        is_animating = False
        render_ui()

        if after_done is not None:
            win.after(120, after_done)

    win.after(interval, step)


# ------------------ AI ------------------


def play_ai_turn() -> None:
    """Let the AI play when it is the AI player's turn."""
    global state

    ai_player = 1
    search_depth = 5

    if is_terminal(state):
        render_ui()
        return

    if state.player != ai_player or is_animating:
        return

    update_status("AI is thinking...")
    win.update_idletasks()

    ai_move = choose_action(state, depth=search_depth)
    animate_move(ai_move, after_done=play_ai_turn)


# ------------------ EVENTS ------------------


def on_click(event) -> None:
    """Handle clicks on the bottom pits."""
    global state

    if is_animating or state.player != 0 or is_terminal(state):
        return

    tags = c.gettags("current")
    clicked_index = None

    for tag in tags:
        parts = tag.split("_")
        if len(parts) == 2 and parts[0] == "bottom" and parts[1].isdigit():
            clicked_index = int(parts[1])
            break

    if clicked_index is None:
        return

    if clicked_index in legal_moves(state):
        animate_move(clicked_index, after_done=play_ai_turn)


def on_pit_enter(index: int) -> None:
    """Highlight a bottom pit on hover."""
    if is_animating or state.player != 0 or is_terminal(state):
        return

    if index in legal_moves(state):
        c.itemconfig(bottom_pits[index], width=4)


def on_pit_leave(index: int) -> None:
    """Remove hover highlight from a bottom pit."""
    c.itemconfig(bottom_pits[index], fill=BOTTOM_PIT_FILL, width=3)


def bind_events() -> None:
    """Bind mouse hover and click events to the bottom pits."""
    for i in bottom_pits:
        c.tag_bind(f"bottom_{i}", "<Button-1>", on_click)
        c.tag_bind(f"bottom_{i}", "<Enter>", lambda _e, idx=i: on_pit_enter(idx))
        c.tag_bind(f"bottom_{i}", "<Leave>", lambda _e, idx=i: on_pit_leave(idx))

    c.config(cursor="hand2")


# ------------------ RUN ------------------


def run_ui() -> None:
    """Set up and start the Kalaha UI."""
    init_game()
    create_window()
    create_stores()
    create_pits()
    create_player_labels()
    create_status_label()
    bind_events()
    render_ui()
    win.mainloop()


if __name__ == "__main__":
    run_ui()