# Graphical User Interface
from io_utils import load_puzzle
from solver import solve
import tkinter as tk

# gui palette
bg_color = "#1e1e2e" # dark navy
cell_shade_a = "#2b2b40" #midnight
cell_shade_b = "#232336" # steel grey
given_digits = "#ffffff" # white
solved_digits = "#4fc3f7" # cyan
cell_font = ("Arial", 18, "bold")

root = tk.Tk()
root.configure(bg=bg_color)
root.title("Sudoku Solver")

grid_frame = tk.Frame(root, bg=bg_color)
grid_frame.pack(padx=20, pady=20)

cells = []
for r in range(9):
    row_widgets=[]
    for c in range(9):
        shade = cell_shade_a if(r // 3 + c // 3) % 2 == 0 else cell_shade_b
        label = tk.Label(grid_frame, text="0", width=4, bg=shade,  height=2, bd=0, font=cell_font)
        left_gap  = 10 if c % 3 == 0 and c !=  0 else 1
        top_gap = 10 if r % 3 == 0 and r != 0 else 1
        label.grid(row=r, column=c, padx=(left_gap,1), pady=(top_gap,1)) # 10 pixels on the left, 1 on the right
        row_widgets.append(label)
    cells.append(row_widgets)

def show_grid(grid, givens):
    for row in range(9):
        for col in range(9):
            value = grid[row][col]
            if value == 0:
                text = ""
            else:
                text = str(value)
            if givens[row][col] != 0:
                color = given_digits
                font = cell_font
            else:
                color = solved_digits
                font = cell_font
            cells[row][col].configure(text=text, fg=color, font=cell_font)

puzzle = load_puzzle("puzzles/easy1.txt")
solution, stats = solve(puzzle)
show_grid(solution, puzzle)


root.mainloop()
