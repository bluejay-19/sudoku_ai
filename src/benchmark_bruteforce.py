# solves each puzzle twice plain and then with MRV + FC
import csv
import os
from solver import solve
from io_utils import load_puzzle

brute_force_puzzle = "puzzles/brute-force.txt"
puzzle_name = os.path.basename(brute_force_puzzle)
puzzle_grid = load_puzzle(brute_force_puzzle)
valid_modes = ["plain", "fc"]
rows = []

print(f"{'puzzle':<14}{'mode':<8}{'nodes':>8}{'backtracks':>12}{'wipeouts':>10}{'time':>12}")

for mode in valid_modes:
    solution, stats = solve(puzzle_grid, mode)
    print(f"{puzzle_name:<14}{mode:<8}{stats['nodes']:>8}{stats['backtracks']:>12}{stats['wipeouts']:>10}{stats['time']:>12.4f}")
    rows.append([puzzle_name, mode, stats['nodes'], stats['backtracks'], stats['wipeouts'], stats['time']])

with open("results/brute-force.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Puzzle', 'Mode', 'Nodes', 'Backtracks', 'Wipeouts', 'Time'])
    writer.writerows(rows)


