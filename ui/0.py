from tkinter import *

# Create main window
win = Tk()
win.title("Kalaha")
win.geometry("900x400")
win.configure(bg="#d2b48c")  # Light wooden background

# Create canvas
c = Canvas(win, width=900, height=400, bg="#c19a6b", highlightthickness=0)
c.pack(pady=20)

# Draw main board
c.create_rectangle(50, 50, 850, 350, fill="#8b5a2b", outline="#5c4033", width=4)

# Draw left and right stores (Kalaha houses)
left_store = c.create_oval(80, 80, 160, 320, fill="#5c3317", outline="#3e2723", width=3)
right_store = c.create_oval(740, 80, 820, 320, fill="#5c3317", outline="#3e2723", width=3)

# Store score labels (UI only)
left_score = Label(win, text="0", font=("Helvetica", 18, "bold"), bg="#c19a6b")
left_score.place(x=110, y=170)

right_score = Label(win, text="0", font=("Helvetica", 18, "bold"), bg="#c19a6b")
right_score.place(x=770, y=170)

# Draw pits (6 top + 6 bottom)
pit_width = 80
pit_height = 80
start_x = 200
spacing = 90

for i in range(6):
    x0 = start_x + i * spacing
    y_top = 90
    y_bottom = 230

    # Top row pits
    c.create_oval(
        x0, y_top,
        x0 + pit_width, y_top + pit_height,
        fill="#5c3317",
        outline="#3e2723",
        width=3
    )

    # Bottom row pits
    c.create_oval(
        x0, y_bottom,
        x0 + pit_width, y_bottom + pit_height,
        fill="#5c3317",
        outline="#3e2723",
        width=3
    )

# Player labels
player1_label = Label(win, text="Player 1", font=("Helvetica", 14, "bold"), bg="#c19a6b")
player1_label.place(x=400, y=330)

player2_label = Label(win, text="Player 2", font=("Helvetica", 14, "bold"), bg="#c19a6b")
player2_label.place(x=400, y=20)

win.mainloop()