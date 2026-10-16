""" Command line entry-point for the Sudoku Solver.

How to run: Use the following command in the terminal 
    python main.py <puzzle_file> [plain|fc]

    plain - plain bracktacking (baseline)
    fc - backtracking with MRV and forward checking (default mode for the solver)

"""
import sys
from io_utils import load_puzzle, print_grid
from solver import solve

# display names for the mode strings solve() expects
labels = {"plain": "Plain backtracking", "fc": "MRV + forward checking"}

def main():
    # the puuzzle file is required the mode is optional
    if len(sys.argv) < 2:
        print("Usage: python main.py <puzzle_file> [plain|fc]")
        return
    path = sys.argv[1]
    # MRV + FC is the main solver, and is used by default when no mode is given manually by the user
    mode = sys.argv[2] if len(sys.argv) > 2 else "fc"

    # a missing file prints the validation message instead of a traceback call
    try:
        grid = load_puzzle(path)
    except(ValueError, FileNotFoundError) as error:
        print(error)
        return

    # shows input first so that the output will reas as puzzle -> result
    print("Puzzle")
    print_grid(grid)

    # solve() will raise ValueError for an unknown mode
    #  Stats for the solver are not printed here;, instead are collected by benchmark.py and shown in the implemented GUI
    try:
        solution, stats = solve(grid, mode)
    except ValueError as error:
        print(error)
        return

    # None means no solution to the input puzzle: either the givens clash, or the search exhausted every option
    if solution is None:
        print(f"No solution found ({labels[mode]})")
    else:
        print(f"Solution (solved with {labels[mode]})")
        print_grid(solution)

# runs only when executed directly, not when imported 
if __name__ == "__main__":
    main()