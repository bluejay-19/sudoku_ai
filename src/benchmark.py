"""
    Benchmark: runs every easy/medium/hard/expert puzzle in both modes, 
    5 times each, and writes results/results.csv
"""

import csv
import os
from solver import solve
from io_utils import load_puzzle

puzzle_files = sorted(os.listdir("puzzles"))
valid_modes = ["plain", "fc"]
accepted_files = ["easy", "medium", "hard", "expert"]
rows = []

print(f"{'puzzle':<14}{'mode':<8}{'nodes':>8}{'backtracks':>12}{'wipeouts':>10}{'time':>12}")

# counts are identical on every run, only time is noisy so store the fastest of the 5 iterations
for puzzle in puzzle_files:
    # only files named easy*/medium*/hard*/expert* are benchmarked any other test files and the brute force puzzles are skipped
    if puzzle.lower().startswith(tuple(accepted_files)):
        puzzle_contents = load_puzzle(f"puzzles/{puzzle}")
        
        for mode in valid_modes:
            best_time = float('inf')
            
            for i in range(5):
                solution, stats = solve(puzzle_contents, mode)
                if stats['time'] < best_time:
                    best_time = stats['time']
            print(f"{puzzle:<14}{mode:<8}{stats['nodes']:>8}{stats['backtracks']:>12}{stats['wipeouts']:>10}{best_time:>12.4f}")
            rows.append([puzzle, mode, stats['nodes'], stats['backtracks'], stats['wipeouts'], best_time])

    
with open("results/results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['Puzzle', 'Mode', 'Nodes', 'Backtracks', 'Wipeouts', 'Time'])
    writer.writerows(rows)
