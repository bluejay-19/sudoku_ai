#  import io_utils for load_puzzle and print_grid functionality
from io_utils import load_puzzle, print_grid

# is valid answers the question: If I wrote a digit in this cell, would that digit repeat already in this cell's row, column or 3x3 box?
def is_valid(grid, row, col, digit):
    if digit in grid[row]:
        return False
    if digit in [grid[i][col] for i in range(9)]:
        return False
    corner_row = row - row % 3
    corner_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if digit == grid[corner_row + i][corner_col + j]:
                return False
    return True

# find_empty answers the question of where is the next blank cell, scans the board and hands back the position of the first 0
def find_empty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row,col
    return None # board is full - solved

# core logic of the solver
def backtrack(grid, stats):
    empty_cell = find_empty(grid)
    if empty_cell is None:
        return True
    row, col = empty_cell
    for digit in range(1,10):
        if is_valid(grid, row, col, digit):
            grid[row][col] = digit
            # counts how many digits the solver placed = amount of work done (search steps measured)
            stats["nodes"] += 1
            result = backtrack(grid, stats)
            if result:
                return True
            grid[row][col] = 0
            # counts how many of those placements turned out to be wrong and need to be undone (amount of work wasted)
            stats["backtracks"] += 1
    return False

if __name__ == "__main__":

    # testing isValid() on easy1.txt
    # print(is_valid(grid, 0, 0, 4)) # row check - return False (4 is in row 0 not in column 0 or the box)
    # print(is_valid(grid, 0, 0, 3))  # col check - return False (3 is in column 0 not in row 0 or the box)
    # print(is_valid(grid, 0, 0, 1)) # box check - return False (1 is in the top-left box, not in row or column 0)
    # print(is_valid(grid, 0, 0, 9)) # returns True (9 is not in row or column 0 and not in the top-left box)
    # print(is_valid(grid, 7, 6, 1))  # returns False - bottom-right box check (cell(7,6) is empty, row7 has 4 & 5, column 6 has 4,5,2,6 & 8, box has a 1 in row 6, 8th column)
    # print(is_valid(grid, 7, 6, 3))  # returns True - (same box as above but there is no three in the row, column or anywhere else in the box)

    # testing find_empty on easy1.txt and bad.txt
    # print(find_empty(grid))
    # grid = load_puzzle("puzzles/bad.txt")
    # print(find_empty(grid))

    # testing backtract on easy1.txt
    grid = load_puzzle("puzzles/easy1.txt")
    stats = {"nodes": 0, "backtracks": 0}
    backtrack(grid, stats)
    print(f"Nodes: {stats['nodes']}, Backtracks: {stats['backtracks']}")
    print_grid(grid)
