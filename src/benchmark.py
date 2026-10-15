# solves each puzzle twice plain and then with MRV + FC
import csv
import os
from solver import solve
from io_utils import load_puzzle

puzzle_files = sorted(os.listdir("puzzles"))
valid_modes = ["plain", "fc"]
accepted_files = ["easy", "medium", "hard", "expert"]
rows = []

for puzzle in puzzle_files:
    if puzzle.lower().startswith(tuple(accepted_files)):
        puzzle_contents = load_puzzle(f"puzzles/{puzzle}")
        for mode in valid_modes:
            solution, stats = solve(puzzle_contents, mode)
            print(f"File name: {puzzle} Mode {mode}")
            print(f"Nodes: {stats['nodes']}")
            print(f"Backtracks: {stats['backtracks']}")
            print(f"Wipeouts: {stats['wipeouts']}")
            print(f"Time: {stats['time']}")
            rows.append([puzzle, mode, stats['nodes'], stats['backtracks'], stats['wipeouts'], stats['time']])
    # else:
    #     print(f"File {puzzle} not accepted.")

with open("results/results.csv", "w") as file:
    newline = ""
    csv.writer()