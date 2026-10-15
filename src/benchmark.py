# solves each puzzle twice plain and then with MRV + FC
import csv
import os
from solver import solve
from io_utils import load_puzzle

puzzle_files = sorted(os.listdir("puzzles"))
valid_modes = ["plain", "fc"]
accepted_files = ["easy", "medium", "hard", "expert"]
rows = []

print(f"{'puzzle':<14}{'mode':<8}{'nodes':>8}{'backtracks':>12}{'wipeouts':>10}{'time':>12}")
for puzzle in puzzle_files:
    if puzzle.lower().startswith(tuple(accepted_files)):
        puzzle_contents = load_puzzle(f"puzzles/{puzzle}")
        for mode in valid_modes:
            solution, stats = solve(puzzle_contents, mode)
            # print(f"File name: {puzzle} Mode {mode}")
            # print(f"Nodes: {stats['nodes']}")
            # print(f"Backtracks: {stats['backtracks']}")
            # print(f"Wipeouts: {stats['wipeouts']}")
            # print(f"Time: {stats['time']}")
            print(f"{puzzle:<14}{mode:<8}{stats['nodes']:>8}{stats['backtracks']:>12}{stats['wipeouts']:>10}{stats['time']:>12.4f}")
            rows.append([puzzle, mode, stats['nodes'], stats['backtracks'], stats['wipeouts'], stats['time']])
    # else:
    #     print(f"File {puzzle} not accepted.")

with open("results/results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['Puzzle', 'Mode', 'Nodes', 'Backtracks', 'Wipeouts', 'Time'])
    writer.writerows(rows)
