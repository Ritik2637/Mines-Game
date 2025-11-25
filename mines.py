import tkinter as tk
from tkinter import messagebox
import random

# Configuration
GRID_SIZE = 16   # bigger grid for full screen
NUM_MINES = 40

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("💣 Minesweeper Game 💣")
        self.master.attributes('-fullscreen', True)  # full screen mode
        self.master.configure(bg="lightgray")
        
        # Get screen dimensions
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        # Calculate button size dynamically
        self.cell_size = min(self.screen_width, self.screen_height) // GRID_SIZE
        
        self.frame = tk.Frame(master, bg="lightgray")
        self.frame.pack(expand=True)

        self.buttons = {}
        self.mines = set()
        self.flags = set()
        self.revealed = set()

        self.create_buttons()
        self.place_mines()

        # Exit full-screen on Escape
        self.master.bind("<Escape>", lambda e: self.master.destroy())

    def create_buttons(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                b = tk.Button(
                    self.frame, width=self.cell_size//10, height=self.cell_size//20,
                    font=("Helvetica", max(self.cell_size//5, 12)),
                    bg="lightblue", command=lambda r=row, c=col: self.reveal(r, c)
                )
                b.bind("<Button-3>", lambda e, r=row, c=col: self.flag(r, c))
                b.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                self.buttons[(row, col)] = b

        # Make the grid expand with window size
        for i in range(GRID_SIZE):
            self.frame.columnconfigure(i, weight=1)
            self.frame.rowconfigure(i, weight=1)

    def place_mines(self):
        while len(self.mines) < NUM_MINES:
            r = random.randint(0, GRID_SIZE-1)
            c = random.randint(0, GRID_SIZE-1)
            self.mines.add((r, c))

    def reveal(self, row, col):
        if (row, col) in self.flags or (row, col) in self.revealed:
            return
        if (row, col) in self.mines:
            self.buttons[(row, col)].config(text="💣", bg="red")
            self.game_over(False)
            return
        count = self.count_mines_around(row, col)
        self.buttons[(row, col)].config(text=str(count) if count > 0 else "", bg="white", relief=tk.SUNKEN)
        self.revealed.add((row, col))
        if count == 0:
            for r in range(max(0, row-1), min(GRID_SIZE, row+2)):
                for c in range(max(0, col-1), min(GRID_SIZE, col+2)):
                    if (r, c) not in self.revealed:
                        self.reveal(r, c)
        if self.check_win():
            self.game_over(True)

    def flag(self, row, col):
        if (row, col) in self.revealed:
            return
        if (row, col) in self.flags:
            self.buttons[(row, col)].config(text="")
            self.flags.remove((row, col))
        else:
            self.buttons[(row, col)].config(text="🚩", fg="red")
            self.flags.add((row, col))

    def count_mines_around(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(GRID_SIZE, row+2)):
            for c in range(max(0, col-1), min(GRID_SIZE, col+2)):
                if (r, c) in self.mines:
                    count += 1
        return count

    def check_win(self):
        return len(self.revealed) == GRID_SIZE*GRID_SIZE - NUM_MINES

    def game_over(self, won):
        for (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣", bg="red")
        msg = "Congratulations! You Won! 🎉" if won else "Game Over! You hit a mine! 💥"
        messagebox.showinfo("Game Over", msg)
        self.master.destroy()


# Run the game
root = tk.Tk()
game = Minesweeper(root)
root.mainloop()
