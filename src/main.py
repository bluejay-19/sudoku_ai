# command line entry point
import sys
from io_utils import load_puzzle, print_grid
from solver import solve

labels = {"plain": "Plain backtracking", "fc": "MRV + forward checking"}

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <puzzle_file> [plain|fc]")
        return
    path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "fc"
    try:
        grid = load_puzzle(path)
    except(ValueError, FileNotFoundError) as error:
        print(error)
        return
    print("Puzzle")
    print_grid(grid)
    try:
        solution, stats = solve(grid, mode)
    except ValueError as error:
        print(error)
        return
    if solution is None:
        print(f"No solution found ({labels[mode]})")
    else:
        print(f"Solution (solved with {labels[mode]})")
        print_grid(solution)

if __name__ == "__main__":
    main()