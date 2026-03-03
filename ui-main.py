from tkinter import *
from game.config import GameConfig
from game.logic import (
    GameState, init_state, legal_moves, apply_move, is_terminal, winner
)

# ------------------ INIT GAME ------------------

cfg = GameConfig(pits_per_side=6)
state = init_state(cfg, stones_per_pit=3)

# ------------------ WINDOW ------------------

win = Tk()
win.title("Kalaha")
win.geometry("900x400")
win.configure(bg="#d2b48c")

c = Canvas(win, width=900, height=400, bg="#c19a6b", highlightthickness=0)
c.pack(pady=20)

c.create_rectangle(50, 50, 850, 350, fill="#8b5a2b", outline="#5c4033", width=4)

# Stores
left_store = c.create_oval(80, 80, 160, 320, fill="#5c3317", outline="#3e2723", width=3)
right_store = c.create_oval(740, 80, 820, 320, fill="#5c3317", outline="#3e2723", width=3)

left_score = Label(win, text="0", font=("Helvetica", 18, "bold"), bg="#c19a6b")
left_score.place(x=110, y=170)

right_score = Label(win, text="0", font=("Helvetica", 18, "bold"), bg="#c19a6b")
right_score.place(x=770, y=170)

# ------------------ PITS ------------------

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


# ------------------ RENDER FUNCTION ------------------

def render_ui():
    global state
    

    if isinstance(state, tuple):
        state = state[0]
    board = state.board

    # Bottom pits (P0) → indices 0 to pits_per_side-1
    for i in range(cfg.pits_per_side):
        value = board[i]
        c.itemconfig(pit_text[("bottom", i)], text=str(value))

    # Top pits (P1) → reversed board mapping
    # Board layout example:
    # bottom: 0..5
    # p0_store
    # top: 6..11 (depends on your config)
    start = cfg.pits_per_side + 1
    end = start + cfg.pits_per_side

    for i in range(cfg.pits_per_side):
        board_index = end - 1 - i  # reverse
        value = board[board_index]
        c.itemconfig(pit_text[("top", i)], text=str(value))

    # Update stores
    left_score.config(text=str(board[cfg.p1_store]))
    right_score.config(text=str(board[cfg.p0_store]))


# ------------------ CLICK HANDLER ------------------

def on_click(event):
    global state

    item = c.find_withtag("current")
    if not item:
        return

    clicked = item[0]

    for index, pit in bottom_pits.items():
        if pit == clicked:
            if index in legal_moves(state):
                state = apply_move(state, index)
                render_ui()
            break


# Bind bottom pits only
for pit in bottom_pits.values():
    c.tag_bind(pit, "<Button-1>", on_click)

# ------------------ PLAYER LABELS ------------------

player1_label = Label(win, text="Player 1", font=("Helvetica", 14, "bold"), bg="#c19a6b")
player1_label.place(x=400, y=330)

player2_label = Label(win, text="Player 2", font=("Helvetica", 14, "bold"), bg="#c19a6b")
player2_label.place(x=400, y=20)

# Initial render
render_ui()

# ------------------ START ------------------
win.mainloop()