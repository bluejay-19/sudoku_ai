"""
    Calls solve() with no search code of its own
    Creates an interface showcasing the 9x9 grid, with the necessary statistics in the side panel
    Load & solve puzzle buttons and a mode dropdown menu 

"""

import tkinter as tk
from tkinter import filedialog
from io_utils import load_puzzle
from solver import solve

# gui palette
bg_color = "#1e1e2e" # dark navy
cell_shade_a = "#2b2b40"    # midnight
cell_shade_b = "#232336"    # steel grey
given_digits = "#ffffff"    # white
solved_digits = "#4fc3f7"   # cyan
cell_font = ("Segoe UI", 18, "bold")
ui_font = ("Segoe UI", 11, "bold")
panel_color = "#262638"     # card background
border_color = "#3b4a6b"
btn_blue = "#1e3a5f"
btn_blue_hover = "#2a4d7d"
btn_green = "#15803d"       # solve: darker green
btn_green_hover = "#16a34a"

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

# Functions 
def show_grid(grid, givens):
    """
    show_grid: draws grid with digits that were also in givens in white 
    and solver-filled digits in cyan

    """
    for row in range(9):
        for col in range(9):
            value = grid[row][col]
            if value == 0:
                text = ""
            else:
                text = str(value)
            if givens[row][col] != 0:
                color = given_digits
            else:
                color = solved_digits
            cells[row][col].configure(text=text, fg=color, font=cell_font)


def load_clicked():
    """
    load_clicked: opens a file dialog, loads and validates the puzzles, 
    shows it and clears the stats in the side panel

    """
    global current_puzzle
    path = filedialog.askopenfilename(filetypes=[("Puzzle files", "*.txt *.csv")])
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
    nodes_label.configure(text="Nodes:")
    backtracks_label.configure(text="Backtracks:")
    wipeouts_label.configure(text="Wipeouts:")
    time_label.configure(text="Time:")


def solve_clicked():
    """
    solve_clicked: solves the loaded puzzle in the chosen mode and updates the grid and stats

    """
    # the window freezes during a long solve (e.g. when testing the brute-force puzzle in plain mode)
    if current_puzzle is None:
        status_label.configure(text="Please load a puzzle first")
        return
    status_label.configure(text="Solving...")
    root.update()
    solution, stats = solve(current_puzzle, modes[mode_var.get()])
    
    nodes_label.configure(text=f"Nodes: {stats['nodes']}")
    backtracks_label.configure(text=f"Backtracks: {stats['backtracks']}")
    wipeouts_label.configure(text=f"Wipeouts: {stats['wipeouts']}")
    time_label.configure(text=f"Time: {stats['time']:.6f}s")
    if solution is None:
        status_label.configure(text="No solution found")
        return
    else:
        show_grid(solution, current_puzzle)
        status_label.configure(text="Solved!")


def make_panel_cards(parent, title):
    """
    make_panel_cards: creates a tilted card frame in the side panel

    """
    card = tk.Frame(parent, bg=panel_color, highlightbackground=border_color, highlightthickness=1)
    card.pack(fill="x", pady=8)
    tk.Label(card, text=title, bg=panel_color, fg="#9fb4d9", font=ui_font).pack(anchor="w", padx=12, pady=(10,4))
    return card


def style_button(parent, text, command, bg, hover_bg):
    """
    style_button: creates a flat button with a hover colour

    """
    btn = tk.Button(parent,text=text, command=command, bg=bg, fg="white", font=ui_font,
                     relief="flat", width=16, pady=10, activebackground=hover_bg, activeforeground="white",  cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn

""" Side panel widgets """
# Status card
status_card = make_panel_cards(panel_frame, "Status")
status_label = tk.Label(status_card, text="Load a puzzle to begin", bg=panel_color, fg="white", font=ui_font, wraplength=200, justify="left")
status_label.pack(anchor="w", padx=12, pady=(0,10))

# Metrics
metrics_card = make_panel_cards(panel_frame, "Metrics")

nodes_label = tk.Label(metrics_card, text="Nodes: ", bg=panel_color, fg="white", font=ui_font)
nodes_label.pack(anchor="w", padx=12, pady=(2,10))

backtracks_label = tk.Label(metrics_card, text="Backtracks: ", bg=panel_color, fg="white", font=ui_font)
backtracks_label.pack(anchor="w", padx=12, pady=(2,10))

wipeouts_label = tk.Label(metrics_card, text="Wipeouts: ", bg=panel_color, fg="white", font=ui_font)
wipeouts_label.pack(anchor="w", padx=12, pady=(2,10))

time_label = tk.Label(metrics_card, text="Time: ", bg=panel_color, fg="white", font=ui_font)
time_label.pack(anchor="w", padx=12, pady=(2,10))

# Controls
controls_card = make_panel_cards(panel_frame, "Controls")

# maps the dropdown label to the mode name that solve() expects
modes = {"Plain": "plain", "MRV + FC": "fc"}
mode_var = tk.StringVar(value="MRV + FC")
mode_dropdown = tk.OptionMenu(controls_card, mode_var, *modes)
mode_dropdown.config(bg="#2a2f4a", fg="white", activebackground=border_color, activeforeground="white",
                     relief="flat", highlightthickness=1, highlightbackground=border_color, width=12, font=ui_font)
mode_dropdown["menu"].configure(bg=panel_color, fg="white", activebackground=border_color)
mode_dropdown.pack(padx=12, pady=6)

load_button = style_button(controls_card, "Load Puzzle", load_clicked, btn_blue, btn_blue_hover)
load_button.pack(padx=12,pady=6)

solve_button = style_button(controls_card, "Solve Puzzle", solve_clicked, btn_green, btn_green_hover)
solve_button.pack(padx=12,pady=6)

root.mainloop()
