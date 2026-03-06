"""Tkinter user interface for Kalaha."""

from tkinter import Canvas, Label, Tk

from game.config import GameConfig
from game.logic import init_state, legal_moves, apply_move

cfg = None
state = None
win = None
c = None
left_score = None
right_score = None
top_pits = {}
bottom_pits = {}
pit_text = {}


def init_game() -> None:
    """Initialize the game configuration and starting state."""
    global cfg, state
    cfg = GameConfig(pits_per_side=6)
    state = init_state(cfg, stones_per_pit=3)


def create_window() -> None:
    """Create the main Tkinter window and canvas."""
    global win, c
    win = Tk()
    win.title("Kalaha")
    win.geometry("900x400")
    win.configure(bg="#d2b48c")

    c = Canvas(win, width=900, height=400, bg="#c19a6b", highlightthickness=0)
    c.pack(pady=20)

    c.create_rectangle(50, 50, 850, 350, fill="#8b5a2b", outline="#5c4033", width=4)


def create_stores() -> None:
    """Draw the stores and create their score labels."""
    global left_score, right_score
    
    c.create_oval(80, 80, 160, 320, fill="#5c3317", outline="#3e2723", width=3)
    c.create_oval(740, 80, 820, 320, fill="#5c3317", outline="#3e2723", width=3)

    left_score = Label(win, text="0", font=("Helvetica", 18, "bold"), bg="#c19a6b")
    left_score.place(x=110, y=170)

    right_score = Label(win, text="0", font=("Helvetica", 18, "bold"), bg="#c19a6b")
    right_score.place(x=770, y=170)


def create_pits() -> None:
    """Draw the top and bottom pits and create their text labels."""
    global top_pits, bottom_pits, pit_text
    
    pit_width = 80
    pit_height = 80
    start_x = 200
    spacing = 90

    top_pits = {}
    bottom_pits = {}

    # store text ids
    pit_text = {}

    for i in range(cfg.pits_per_side):
        x0 = start_x + i * spacing
        y_top = 90
        y_bottom = 230

        # TOP ROW (player 1)
        top_pit = c.create_oval(
            x0, y_top,
            x0 + pit_width, y_top + pit_height,
            fill="#3e2723",
            outline="#2c1b14",
            width=3
        )
        top_pits[i] = top_pit

        top_text = c.create_text(
            x0 + pit_width/2,
            y_top + pit_height/2,
            text="0",
            fill="white",
            font=("Helvetica", 14, "bold")
        )
        pit_text[("top", i)] = top_text

        # BOTTOM ROW (player 0)
        bottom_pit = c.create_oval(
            x0, y_bottom,
            x0 + pit_width, y_bottom + pit_height,
            fill="#5c3317",
            outline="#3e2723",
            width=3
        )
        bottom_pits[i] = bottom_pit

        bottom_text = c.create_text(
            x0 + pit_width/2,
            y_bottom + pit_height/2,
            text="0",
            fill="white",
            font=("Helvetica", 14, "bold")
        )
        pit_text[("bottom", i)] = bottom_text


def create_player_labels() -> None:
    """Create the player labels."""
    player1_label = Label(
        win, text="Player 1", font=("Helvetica", 14, "bold"), bg="#c19a6b"
    )
    player1_label.place(x=400, y=330)

    player2_label = Label(
        win, text="Player 2", font=("Helvetica", 14, "bold"), bg="#c19a6b"
    )
    player2_label.place(x=400, y=20)


def render_ui() -> None:
    """Update the board values shown in the UI."""    
    board = state.board

    # Bottom pits (player 0): indices 0 to pits_per_side - 1
    for i in range(cfg.pits_per_side):
        value = board[i]
        c.itemconfig(pit_text[("bottom", i)], text=str(value))

    # top pits (player 1): reversed visual order
    start = cfg.pits_per_side + 1
    end = start + cfg.pits_per_side

    for i in range(cfg.pits_per_side):
        board_index = end - 1 - i  # reverse
        value = board[board_index]
        c.itemconfig(pit_text[("top", i)], text=str(value))

    # Update stores
    left_score.config(text=str(board[cfg.p1_store]))
    right_score.config(text=str(board[cfg.p0_store]))


def on_click(event) -> None:
    """Handle clicks on the bottom pits."""
    global state

    item = c.find_withtag("current")
    if not item:
        return

    clicked = item[0]

    for index, pit in bottom_pits.items():
        text_id = pit_text[("bottom", index)]
        
        if clicked == pit or clicked == text_id:
            if index in legal_moves(state):
                state, _ = apply_move(state, index)
                render_ui()
            break


def bind_events() -> None:
    """Bind mouse click events to the bottom pits."""
    for i, pit in bottom_pits.items():
        c.tag_bind(pit, "<Button-1>", on_click)
        c.tag_bind(pit_text[("bottom", i)], "<Button-1>", on_click)
        # There are cool options for the cursor
        # Try: heart, star, pirate, spider, spraycan
        c.config(cursor="circle")


def run_ui() -> None:
    """Set up and start the Kalaha UI."""
    init_game()
    create_window()
    create_stores()
    create_pits()
    create_player_labels()
    bind_events()
    render_ui()
    win.mainloop()
    
    
if __name__ == "__main__":
    run_ui()