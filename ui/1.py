from tkinter import *

root = Tk()
root.title("Kalaha / Mancala - Board")
root.configure(bg="#2e1a0f")  # dark wood-ish background for window

# Fixed window size - good proportions for Kalaha
WIDTH = 780
HEIGHT = 420
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

# Main canvas
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="#3c2a1e",  # warm wood color
                highlightthickness=0)
canvas.pack()

# Background - subtle wood texture simulation
canvas.create_rectangle(20, 20, WIDTH-20, HEIGHT-20, fill="#5c4033", outline="#8B5A2B", width=6)
canvas.create_rectangle(35, 35, WIDTH-35, HEIGHT-35, fill="#8B6F47", outline="#A67C52", width=2)

# ───────────────────────────────────────────────
#          LEFT STORE (Player 2 / Bottom player)
# ───────────────────────────────────────────────
canvas.create_oval(40, 100, 140, 320, fill="#4a2c15", outline="#8B5A2B", width=4)   # outer shadow
canvas.create_oval(55, 115, 125, 305, fill="#d4a373", outline="#e8c39e", width=3)   # main store
canvas.create_oval(65, 125, 115, 295, fill="#e6c88f", outline="")                   # highlight

# Store label
canvas.create_text(90, 70, text="PLAYER 2", fill="white", font=("Helvetica", 14, "bold"))
canvas.create_text(90, 345, text="STORE", fill="#e0d4b0", font=("Helvetica", 11))

# ───────────────────────────────────────────────
#         RIGHT STORE (Player 1 / Top player)
# ───────────────────────────────────────────────
canvas.create_oval(WIDTH-140, 100, WIDTH-40, 320, fill="#4a2c15", outline="#8B5A2B", width=4)
canvas.create_oval(WIDTH-125, 115, WIDTH-55, 305, fill="#d4a373", outline="#e8c39e", width=3)
canvas.create_oval(WIDTH-115, 125, WIDTH-65, 295, fill="#e6c88f", outline="")

canvas.create_text(WIDTH-90, 70, text="PLAYER 1", fill="white", font=("Helvetica", 14, "bold"))
canvas.create_text(WIDTH-90, 345, text="STORE", fill="#e0d4b0", font=("Helvetica", 11))

# ───────────────────────────────────────────────
#           6 + 6 playing pits (houses)
# ───────────────────────────────────────────────
pit_width = 68
pit_height = 68
start_x = 170
gap = 82

# Top row (Player 1's side - seeds go counterclockwise → right to left)
for i in range(6):
    x = start_x + i * gap
    # shadow / depth
    canvas.create_oval(x-4, 115-4, x+pit_width+4, 115+pit_height+4, fill="#3a220f", outline="")
    # main pit
    canvas.create_oval(x, 115, x+pit_width, 115+pit_height, fill="#a67c52", outline="#8B5A2B", width=2)
    # inner highlight
    canvas.create_oval(x+6, 121, x+pit_width-6, 115+pit_height-6, fill="#d9b38c", outline="", stipple="gray50")

    # Small number placeholder (you can remove later or use for debugging)
    # canvas.create_text(x + pit_width//2, 115 + pit_height//2, text=str(6-i), fill="#4a2c15", font=("Arial", 11, "bold"))

# Bottom row (Player 2's side - left to right)
for i in range(6):
    x = start_x + i * gap
    # shadow
    canvas.create_oval(x-4, 235-4, x+pit_width+4, 235+pit_height+4, fill="#3a220f", outline="")
    # main pit
    canvas.create_oval(x, 235, x+pit_width, 235+pit_height, fill="#a67c52", outline="#8B5A2B", width=2)
    # inner highlight
    canvas.create_oval(x+6, 241, x+pit_width-6, 235+pit_height-6, fill="#d9b38c", outline="", stipple="gray50")

    # canvas.create_text(x + pit_width//2, 235 + pit_height//2, text=str(i+1), fill="#4a2c15", font=("Arial", 11, "bold"))

# Title / decoration
canvas.create_text(WIDTH//2, 30, text="KALAHA", fill="#e8d5a3", font=("Helvetica", 22, "bold"), 
                   stipple="gray25")
canvas.create_text(WIDTH//2, HEIGHT-25, text="Traditional Mancala Board", fill="#c9a875", 
                   font=("Helvetica", 10, "italic"))

root.mainloop()