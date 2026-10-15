# Graphical User Interface

import tkinter as tk
from tkinter import filedialog
from io_utils import load_puzzle
from solver import solve

# gui palette
bg_color = "#1e1e2e" # dark navy
cell_shade_a = "#2b2b40" #midnight
cell_shade_b = "#232336" # steel grey
given_digits = "#ffffff" # white
solved_digits = "#4fc3f7" # cyan
cell_font = ("Times New Roman", 18, "bold")

# shared state
current_puzzle = None

# window
root = tk.Tk()
root.configure(bg=bg_color)
root.title("Sudoku Solver")

# frames
grid_frame = tk.Frame(root, bg=bg_color)
grid_frame.pack(padx=20, pady=20, side="left")
panel_frame = tk.Frame(root, bg=bg_color)
panel_frame.pack(padx=20, pady=20, side="right")

# build the 81 cells of the sudoku grid
cells = []
for r in range(9):
    row_widgets=[]
    for c in range(9):
        shade = cell_shade_a if(r // 3 + c // 3) % 2 == 0 else cell_shade_b
        label = tk.Label(grid_frame, text="", width=4, bg=shade,  height=2, bd=0, font=cell_font)
        left_gap  = 10 if c % 3 == 0 and c !=  0 else 1
        top_gap = 10 if r % 3 == 0 and r != 0 else 1
        label.grid(row=r, column=c, padx=(left_gap,1), pady=(top_gap,1)) # 10 pixels on the left, 1 on the right
        row_widgets.append(label)
    cells.append(row_widgets)

# functions
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

def load_clicked():
    global current_puzzle
    path = filedialog.askopenfilename()
    if not path:
        return # user cancelled
    try:
        puzzle = load_puzzle(path)
    except (ValueError, FileNotFoundError) as error:
        status_label.configure(text=str(error))
        return
    current_puzzle = puzzle
    show_grid(puzzle, puzzle)
    status_label.configure(text="Puzzle loaded")

def solve_clicked():
    if current_puzzle is None:
        status_label.configure(text="Please load a puzzle first")
        return
    solution, stats = solve(current_puzzle, modes[mode_var.get()])
    if solution is None:
        status_label.configure(text="No solution found")
        return
    show_grid(solution, current_puzzle)
    status_label.configure(text="Solved!")




# side panel widgets
# load button
status_label = tk.Label(panel_frame, text="Load a puzzle to begin", bg=bg_color, fg="white")
status_label.pack(pady=10)
# nodes label, backtracks label, wipeouts label and time label to be input
load_button = tk.Button(panel_frame, text="Load Puzzle", command=load_clicked, bg=bg_color, fg="white")
load_button.pack(pady=5)

# mode dropdown & solve button
modes = {"Plain": "plain", "MRV + FC": "fc"}
mode_var = tk.StringVar(value="Plain")
mode_dropdown = tk.OptionMenu(panel_frame, mode_var, *modes)
mode_dropdown.pack(pady=5)
solve_button = tk.Button(panel_frame, text="Solve Puzzle", command=solve_clicked, bg=bg_color, fg="white")
solve_button.pack(pady=5)






root.mainloop()
