#  import io_utils for load_puzzle and print_grid functionality
import time
import copy

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

# core logic of the solver - plain backtracking
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

# domains - list of digits that could still go in that cell
# a filled cell only has one possible value (the one already there), a blank cell has many digits dont clash
def compute_domains(grid):
    domain = []
    for row in range(9):
        current_row = []
        for col in range(9):
            set_of_cells = set()
            # check if the cell is already filled
            if grid[row][col] != 0:
                set_of_cells.add(grid[row][col]) # set should hold the current digit
            else:
                # loop through all possible digits for a blank cell
                for digit in range(1,10):
                    if is_valid(grid, row, col, digit):
                        set_of_cells.add(digit)
            current_row.append(set_of_cells)
        domain.append(current_row)
    return domain

# MRV - picks the blank cell with the fewest options first
# forced moves get made early without guessing, doomed branches die near the top of the search tree
# before the solver has to build a huge subtree under them
# nodes and backtrakcs values drop which is an improvement from plain backtracking
def select_mrv_cell(grid, domain):
    # how many options does the most constrained cell seen so far have
    best_size = 10
    # which cell is the most constrained cell
    best_cell = None
    for row in range(9):
        for col in range(9):
            # skip filled cells
            if grid[row][col] != 0:
                continue
            # compare domain's size with the best size
            if len(domain[row][col]) < best_size:
                best_size = len(domain[row][col])
                best_cell = (row, col)
    return best_cell

# FORWARD CHECKING
# returns the 20 cells that share a row, column or box with (row,col)
def get_peers(row, col):
    peers = set()
    corner_row = row - row % 3
    corner_col = col - col % 3

    # cells in the same row: can't repeat this cell's digit
    for i in range(9):
        peers.add((i, col))
    # cells in the same column
    for j in range(9):
        peers.add((row,j))
    # cells in the same 3x3 box (this is what adds the 4 extra peers the row and column miss)
    for m in range(3):
        for n in range(3):
            peers.add((corner_row + m, corner_col + n))
    # a cell is not its own peer; otherwise forward checking would strip the digit from the cell that was just filled
    peers.discard((row,col))
    return peers

# place a digit at a cell then tell every peer cell it can no longer use the placed digit
def assign(grid, domain, row, col, digit):
    # when search picks up a digit from the domain it is valid by construction because a cell's domain is already a list of digits that fit
    # put the digit in the grid
    grid[row][col] = digit
    domain[row][col] = set({digit})
    for r, c in get_peers(row,col):
        # this digit is now taken in the peer's row/column/box
        domain[r][c].discard(digit)
        if len(domain[r][c]) == 0:
            return False
    return True

# recursive forward checking search
# same skeleton as backtrack but three differences: it picks the cell with MRV, it only tries digits from that cell's domain, and it then uses assign to place them
# returns the solved grid or None, and works with copies of the grid and domain
def fc_search (grid, domain, stats):
    cell = select_mrv_cell(grid, domain)
    if cell is None:
        return grid
    row, col = cell
    for digit in domain[row][col]:
        # fresh copy per digit so a failed attempt leaves nothing behind (this is the undo)
        grid_copy = copy.deepcopy(grid)
        domain_copy = copy.deepcopy(domain)
        # nodes = digits tried
        stats["nodes"] += 1
        if assign(grid_copy, domain_copy, row, col, digit):
            result = fc_search(grid_copy, domain_copy, stats)
            if result is not None:
                return result
        else:
            # wipeouts shows how many dead ends were detected before the search goes deeper
            stats["wipeouts"] += 1
        # counted whether assign failed immediately or the deeper search failed
        stats["backtracks"] += 1
    return None

# helper function that performs pre-checks answering the question "would this digit be allowed here if the cell were empty" if not it clashes with another given digit before the solving even start
def conflict_check(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                digit = grid[row][col]
                grid[row][col] = 0      # empty the cell
                value_fit = is_valid(grid, row, col, digit)
                grid[row][col] = digit
                if not value_fit:
                    return True
    return False # no conflicts found


def solve(grid):
    grid_copy = copy.deepcopy(grid)
    stats ={"nodes": 0, "backtracks": 0, "wipeouts": 0}

    # conflict check on the existing grid values (before solving)
    if conflict_check(grid_copy):
        stats["time"] = 0
        return None, stats

    start_time = time.perf_counter()
    result = backtrack(grid_copy, stats)
    end_time = time.perf_counter()
    stats["time"] = end_time - start_time
    if result is True:
        return grid_copy, stats
    else:
        return None, stats

# TESTING EXAMPLES

if __name__ == "__main__":
    #print_grid(grid)

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

    # testing backtrack on easy1.txt
    #grid = load_puzzle("puzzles/hard1.txt")
    # stats = {"nodes": 0, "backtracks": 0}
    # backtrack(grid, stats)
    # print(f"Nodes: {stats['nodes']}, Backtracks: {stats['backtracks']}")
    # print_grid(grid)

    # testing solve
    # grid = load_puzzle("puzzles/bad.txt")
    # result, stats = solve(grid)
    # print(f"Nodes: {stats['nodes']}, Backtracks: {stats['backtracks']}, Time: {stats['time']}")
    # if result is None:
    #     print("No solution found")
    # else:
    #     print_grid(result)

    # testing compute_domain & select_mrv_cell
    # grid = load_puzzle("puzzles/medium1.txt")
    # domain = compute_domains(grid)
    # print(select_mrv_cell(grid, domain))
    # print(domain[0])

    # # rigging a cell to have a smaller domain than the current smallest domain
    # # smallest domain for medium1.txt is (0,0)
    # domain[8][8] = {3}
    # print(select_mrv_cell(grid, domain))

    # testing select_mrv_cell on a solved grid - correctly returns None (there is nothing left to fill in a solved grid)
    # grid = load_puzzle("puzzles/medium2.txt")
    # solution, stats = solve(grid)
    # domain = compute_domains(solution)
    # print(select_mrv_cell(solution, domain))

    # Testing get_peers
    # grid = load_puzzle("puzzles/easy1.txt")
    # domain = compute_domains(grid)
    # row,column and box loops produce the right number of cells with overlaps counted once == 20
    # print(len(get_peers(0,0)))
    # same logic works from a different position in the grid (this test makes sure the corner arithmetic works with a cell that sits in the middle)
    # print(len(get_peers(4, 4)))
    # discard functionality worked - False (A cell must not count as its own peer)
    # print((0,0) in get_peers(0,0))
    # Box loop works - True (1,1) shares only a box with (0,0) not a row or column
    # print((1, 1) in get_peers(0, 0))
    # catches loops that add too much
    # print((3, 3) in get_peers(0, 0))

    #Testing assign
    # grid = load_puzzle("puzzles/easy1.txt")
    # grid_copy = copy.deepcopy(grid)
    # domain_copy = compute_domains(grid_copy)
    # domain_copy[0][1] = {9}
    # print(assign(grid_copy, domain_copy, 0, 0, 9 ))
    # print(grid_copy[0][0], domain_copy[0][1])
    # print(domain_copy[0][3])

    # testing fc_search
    grid = load_puzzle("puzzles/expert1.txt")
    domain = compute_domains(grid)
    fc_stats = {"nodes" : 0, "backtracks": 0, "wipeouts": 0}
    fc_solution = fc_search(grid, domain, fc_stats)
    plain_solution, plain_stats = solve(grid)
    if fc_solution is None:
        print("No solution found")
    print_grid(fc_solution)
    print(fc_solution == plain_solution)
    print(fc_stats)
    print(plain_stats)


