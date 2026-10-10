# command line entry point
import sys
from io_utils import load_puzzle, print_grid
from solver import solve

def main():
    if len(sys.argv) < 2:
        print("No valid path was input")
        return
    path = sys.argv[1]
    try:
        grid = load_puzzle(path)
    except(ValueError, FileNotFoundError) as error:
        print(error)
        return
    print("Puzzle")
    print_grid(grid)
    solution, stats = solve(grid)
    if solution is None:
        print("No solution found")
    else:
        print("Solution")
        print_grid(solution)

if __name__ == "__main__":
    main()