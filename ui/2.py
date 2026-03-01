"""
Kalaha (Mancala) Board Game UI
Beautiful, polished interface using tkinter only.
No game logic - UI visuals only.
"""

import tkinter as tk
from tkinter import font


# ─── Palette ──────────────────────────────────────────────────────────────────
BG_DARK       = "#1a0f00"   # deep walnut
BOARD_COLOR   = "#6b3a1f"   # rich mahogany
BOARD_EDGE    = "#3d1f0a"   # dark wood border
PIT_FILL      = "#2e1505"   # pit hollow
PIT_RIM       = "#8b5e3c"   # carved rim
STONE_PLAYER1 = "#e8c96a"   # golden amber
STONE_PLAYER2 = "#4fc3d0"   # ocean teal
SHADOW        = "#0d0800"
SCORE_BG      = "#3d1f0a"
SCORE_FG      = "#f5e6c8"
LABEL_FG      = "#c49a5a"
TITLE_FG      = "#f5d98a"
TURN_FG       = "#ffffff"
HIGHLIGHT     = "#ffcc44"

BOARD_W, BOARD_H = 820, 500
WIN_W,  WIN_H    = 860, 560


def draw_rounded_rect(canvas, x1, y1, x2, y2, r=20, **kwargs):
    """Draw a rounded rectangle on a canvas."""
    canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90,  extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0,   extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="pieslice", **kwargs)
    canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
    canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)


def draw_stones(canvas, cx, cy, count, color, pit_r=42):
    """Draw stones inside a pit centred at (cx, cy)."""
    if count == 0:
        return
    # Show up to 12 stones; beyond that show a number badge
    max_draw = min(count, 12)
    import math
    r_stone = 7 if count <= 6 else 5
    spread   = pit_r * 0.55

    positions = []
    if max_draw == 1:
        positions = [(0, 0)]
    elif max_draw <= 4:
        for i in range(max_draw):
            a = i * (2*math.pi / max_draw) + math.pi/4
            positions.append((spread * 0.5 * math.cos(a), spread * 0.5 * math.sin(a)))
    else:
        inner = min(max_draw // 2, 4)
        outer = max_draw - inner
        for i in range(inner):
            a = i * (2*math.pi / inner)
            positions.append((spread * 0.35 * math.cos(a), spread * 0.35 * math.sin(a)))
        for i in range(outer):
            a = i * (2*math.pi / outer) + math.pi/outer
            positions.append((spread * 0.75 * math.cos(a), spread * 0.75 * math.sin(a)))

    for px, py in positions[:max_draw]:
        sx, sy = cx + px, cy + py
        # shadow
        canvas.create_oval(sx - r_stone + 2, sy - r_stone + 2,
                            sx + r_stone + 2, sy + r_stone + 2,
                            fill="#111111", outline="")
        # stone body
        canvas.create_oval(sx - r_stone, sy - r_stone,
                            sx + r_stone, sy + r_stone,
                            fill=color, outline="", width=0)
        # highlight glint
        canvas.create_oval(sx - r_stone + 2, sy - r_stone + 2,
                            sx - r_stone//2, sy - r_stone//2,
                            fill="#dddddd", outline="")

    if count > 12:
        canvas.create_text(cx, cy, text=str(count),
                           font=("Georgia", 11, "bold"), fill=TITLE_FG)


def build_ui():
    win = tk.Tk()
    win.title("Kalaha")
    win.geometry(f"{WIN_W}x{WIN_H}")
    win.resizable(False, False)
    win.configure(bg=BG_DARK)

    # ── Title ──────────────────────────────────────────────────────────────────
    title_font = tk.font.Font(family="Georgia", size=22, weight="bold")
    title = tk.Label(win, text="✦  K A L A H A  ✦",
                     font=title_font, bg=BG_DARK, fg=TITLE_FG)
    title.pack(pady=(14, 0))

    # ── Canvas ─────────────────────────────────────────────────────────────────
    c = tk.Canvas(win, width=BOARD_W, height=BOARD_H,
                  bg=BG_DARK, highlightthickness=0)
    c.pack(padx=20, pady=8)

    ox, oy = 20, 30   # board origin offset

    # ── Board shadow ───────────────────────────────────────────────────────────
    c.create_rectangle(ox+8, oy+8, ox+BOARD_W-56, oy+BOARD_H-66,
                       fill=SHADOW, outline="", width=0)

    # ── Board body ─────────────────────────────────────────────────────────────
    draw_rounded_rect(c, ox, oy, ox+BOARD_W-64, oy+BOARD_H-74,
                      r=34, fill=BOARD_COLOR, outline=BOARD_EDGE, width=4)

    # Wood grain lines (decorative)
    for i in range(5):
        y_grain = oy + 60 + i * 60
        c.create_line(ox+20, y_grain, ox+BOARD_W-84, y_grain,
                      fill="#7a4422", width=1, dash=(12, 8))

    # ── Kalah stores (left & right big pits) ──────────────────────────────────
    store_r = 58
    # Left Kalah  (Player 2 scores here)
    lkx, lky = ox + 68, oy + (BOARD_H-74)//2
    c.create_oval(lkx-store_r-3, lky-store_r-3, lkx+store_r+3, lky+store_r+3,
                  fill=BOARD_EDGE, outline="")
    c.create_oval(lkx-store_r, lky-store_r, lkx+store_r, lky+store_r,
                  fill=PIT_FILL, outline=PIT_RIM, width=3)
    draw_stones(c, lkx, lky, 0, STONE_PLAYER2, pit_r=store_r-10)
    c.create_text(lkx, lky+store_r+18, text="P2  Store",
                  font=("Georgia", 9, "italic"), fill=LABEL_FG)

    # Right Kalah (Player 1 scores here)
    rkx, rky = ox + BOARD_W - 64 - 68, oy + (BOARD_H-74)//2
    c.create_oval(rkx-store_r-3, rky-store_r-3, rkx+store_r+3, rky+store_r+3,
                  fill=BOARD_EDGE, outline="")
    c.create_oval(rkx-store_r, rky-store_r, rkx+store_r, rky+store_r,
                  fill=PIT_FILL, outline=PIT_RIM, width=3)
    draw_stones(c, rkx, rky, 0, STONE_PLAYER1, pit_r=store_r-10)
    c.create_text(rkx, rky+store_r+18, text="P1  Store",
                  font=("Georgia", 9, "italic"), fill=LABEL_FG)

    # ── 6 pits per player ─────────────────────────────────────────────────────
    pit_r   = 40
    pit_gap = 10
    usable  = (rkx - store_r) - (lkx + store_r)
    pit_spacing = usable / 6
    pit_start   = lkx + store_r + pit_spacing / 2

    # Row y-centres
    top_y = oy + 68       # Player 2 pits (top row)
    bot_y = oy + (BOARD_H-74) - 68   # Player 1 pits (bottom row)

    # Initial stone count per pit
    initial_stones = 4

    for i in range(6):
        cx_pit = pit_start + i * pit_spacing

        # ── Top row  (Player 2, indices 0-5 → displayed right-to-left) ────────
        # shadow
        c.create_oval(cx_pit-pit_r+3, top_y-pit_r+3,
                      cx_pit+pit_r+3, top_y+pit_r+3,
                      fill=SHADOW, outline="")
        # rim
        c.create_oval(cx_pit-pit_r-3, top_y-pit_r-3,
                      cx_pit+pit_r+3, top_y+pit_r+3,
                      fill=BOARD_EDGE, outline="")
        # hollow
        c.create_oval(cx_pit-pit_r, top_y-pit_r,
                      cx_pit+pit_r, top_y+pit_r,
                      fill=PIT_FILL, outline=PIT_RIM, width=2)
        draw_stones(c, cx_pit, top_y, initial_stones, STONE_PLAYER2, pit_r=pit_r-6)
        # pit number label (P2 goes right→left)
        c.create_text(cx_pit, top_y - pit_r - 12, text=str(6 - i),
                      font=("Georgia", 8), fill=LABEL_FG)

        # ── Bottom row  (Player 1, indices 0-5 left-to-right) ─────────────────
        c.create_oval(cx_pit-pit_r+3, bot_y-pit_r+3,
                      cx_pit+pit_r+3, bot_y+pit_r+3,
                      fill=SHADOW, outline="")
        c.create_oval(cx_pit-pit_r-3, bot_y-pit_r-3,
                      cx_pit+pit_r+3, bot_y+pit_r+3,
                      fill=BOARD_EDGE, outline="")
        c.create_oval(cx_pit-pit_r, bot_y-pit_r,
                      cx_pit+pit_r, bot_y+pit_r,
                      fill=PIT_FILL, outline=PIT_RIM, width=2)
        draw_stones(c, cx_pit, bot_y, initial_stones, STONE_PLAYER1, pit_r=pit_r-6)
        c.create_text(cx_pit, bot_y + pit_r + 12, text=str(i + 1),
                      font=("Georgia", 8), fill=LABEL_FG)

    # ── Player name labels ─────────────────────────────────────────────────────
    mid_x = (lkx + rkx) // 2
    c.create_text(mid_x, top_y - pit_r - 28,
                  text="▲  PLAYER 2",
                  font=("Georgia", 11, "bold"), fill=STONE_PLAYER2)
    c.create_text(mid_x, bot_y + pit_r + 28,
                  text="PLAYER 1  ▼",
                  font=("Georgia", 11, "bold"), fill=STONE_PLAYER1)

    # ── Score bar (below canvas) ───────────────────────────────────────────────
    score_frame = tk.Frame(win, bg=BG_DARK)
    score_frame.pack(fill="x", padx=40, pady=(0, 12))

    score_font = tk.font.Font(family="Georgia", size=13, weight="bold")
    lbl_font   = tk.font.Font(family="Georgia", size=9)

    # Player 2 score block
    p2_frame = tk.Frame(score_frame, bg=SCORE_BG, bd=0,
                        highlightbackground=STONE_PLAYER2,
                        highlightthickness=2)
    p2_frame.pack(side="left", padx=(0, 10), ipadx=16, ipady=6)
    tk.Label(p2_frame, text="PLAYER 2", font=lbl_font,
             bg=SCORE_BG, fg=STONE_PLAYER2).pack()
    tk.Label(p2_frame, text="0", font=score_font,
             bg=SCORE_BG, fg=SCORE_FG).pack()

    # Turn indicator (centre)
    turn_var = tk.StringVar(value="Player 1's Turn")
    turn_lbl = tk.Label(score_frame, textvariable=turn_var,
                        font=tk.font.Font(family="Georgia", size=12, weight="bold"),
                        bg=BG_DARK, fg=HIGHLIGHT)
    turn_lbl.pack(side="left", expand=True)

    # Player 1 score block
    p1_frame = tk.Frame(score_frame, bg=SCORE_BG, bd=0,
                        highlightbackground=STONE_PLAYER1,
                        highlightthickness=2)
    p1_frame.pack(side="right", padx=(10, 0), ipadx=16, ipady=6)
    tk.Label(p1_frame, text="PLAYER 1", font=lbl_font,
             bg=SCORE_BG, fg=STONE_PLAYER1).pack()
    tk.Label(p1_frame, text="0", font=score_font,
             bg=SCORE_BG, fg=SCORE_FG).pack()

    win.mainloop()


if __name__ == "__main__":
    build_ui()