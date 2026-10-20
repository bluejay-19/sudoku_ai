""" Sudoky solving logic: two searches plus the solve() entry point

plain - plain backtracking, always fills the first blank in the puzzle, this is the baseline 
fc - backtracking with MRV cell selection and forward checking 

There is nothing in this file that prints, making it reusable by main.py, gui.py and benchmark.py

During initial development of the code there were tests done in the file itself, ensuring the solver actually worked.
"""

import time
import copy

from io_utils import load_puzzle, print_grid

def is_valid(grid, row, col, digit):
    """ Return True if the digit can be put at the position (row,col) without repeating in
    its row, colum or 3x3 box. Never modifies the actual grid.  """

    # row check
    if digit in grid[row]:
        return False
    # column check: collecting the column into a list first
    if digit in [grid[i][col] for i in range(9)]:
        return False
    # box check: (corner_row, corner_col)forms the top left cell of the 3x3 box
    corner_row = row - row % 3
    corner_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if digit == grid[corner_row + i][corner_col + j]:
                return False
    return True


def find_empty(grid):
    """Returns (row,col) of the first blank that appears in the input puzzle in reading order. or None if the puzzle is full"""

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row,col
    return None # no blanks left, board is full/solved


# core logic of the solver 
def backtrack(grid, stats):
    """Plain backtracking will fill the sudoky grid in place and return True if solved.

    stats["nodes"]  = digits placed (search effort)
    stats["backtracks"] = placements later done (wasted effort)  """

    empty_cell = find_empty(grid)
    if empty_cell is None:
        return True      # base case: Board is full 
    row, col = empty_cell
    for digit in range(1,10):
        if is_valid(grid, row, col, digit):
            grid[row][col] = digit
            stats["nodes"] += 1
            result = backtrack(grid, stats)
            if result:
                return True # keep the digits, the board is now the solution
            # dead end below: undo so the next digits starts from a clean board
            grid[row][col] = 0
            stats["backtracks"] += 1
    return False    # no digit worked, so the caller has to undo its own move



def compute_domains(grid):
    """ Build the domains: a 9x9 list of sets that mirror the sudoku grid, where 
    domain[r][c] holds the digits that are still legal at that cell. 
    A filled cell holds a set with just its own digit.  """
    
    domain = []
    for row in range(9):
        current_row = []
        for col in range(9):
            set_of_cells = set()
            # check if the cell is already filled
            if grid[row][col] != 0:
                set_of_cells.add(grid[row][col]) # set should hold the current digit
            else:
                # blank cell: keep every digit that does not class with the rpw/column/box
                for digit in range(1,10):
                    if is_valid(grid, row, col, digit):
                        set_of_cells.add(digit)
            current_row.append(set_of_cells)
        domain.append(current_row)
    return domain


def select_mrv_cell(grid, domain):
    """ MRV (Minimum Remaining Values): return (row, col) of the blank cell that has the smallest domain, 
    or None if there are no blanks left in the sudoku grid. 
    Ties go to the firt cell in reading order; the degree heuristic is not used

    Forced moves get made early without guessing and doomed branches die near the top of the search tree
    Before the solver has to build a huge subtree under them 
    Nodes and backtrack values drop which is an improvement from plain backtracking     """

    best_size = 10   # larger than any possible domain, allowing the first blank to always win
    best_cell = None    # the most constrained cell
    for row in range(9):
        for col in range(9):
            # skip filled cells
            if grid[row][col] != 0:
                continue    # only remaining candidates are blanks
            if len(domain[row][col]) < best_size:   # compare domain's size with the best size using a strict '<' to get the earliest tie
                best_size = len(domain[row][col])
                best_cell = (row, col)
    return best_cell

# FORWARD CHECKING
def get_peers(row, col):
    """ Return the 20 cells that share a row, column or 3x3 box with (row,col).
    Usess positions only, the grid is not needed.   """
    peers = set()
    corner_row = row - row % 3
    corner_col = col - col % 3

    # cells in the same columnn (row number changes)
    for i in range(9):
        peers.add((i, col))
    # cells in the same row (column number changes)
    for j in range(9):
        peers.add((row,j))
    # cells in the same 3x3 box: adds the 4 peers the row and column miss. The set absorbs the overlaps, giving 20 not 24
    for m in range(3):
        for n in range(3):
            peers.add((corner_row + m, corner_col + n))
    # a cell is not its own peer, or forward checking would strip the digit from the cell that was just filled
    peers.discard((row,col))
    return peers


def assign(grid, domain, row, col, digit):
    """ Place digit at (row,col) and remove it from every peer's domain. 

    Returns false as soon as a peer's domain becomes empty (a dead end found early), True otherwise. 
    Edits the grid and domain in place and it may leave them partly updated on failure, so callers
    must pass copies. No validity check is needed: the digit comes from the cell's domain.

    When search picks up a digit from the domain it is valid by construction because a 
    cell's domain is already a list of digits that fit. Put the digit in the grid.  """
    grid[row][col] = digit
    domain[row][col] = set({digit})
    for r, c in get_peers(row,col):
        domain[r][c].discard(digit)  # this digit is now taken in the peer's row/column/box
        if len(domain[r][c]) == 0:
            return False     # wipeout: this peer has no legal digit left 
    return True


def fc_search (grid, domain, stats):
    """ Backtracking with MRV and forward checking.
    Returns the solved grid, or None if no solution exists. Doesn't modify its arguments: 
    each atttempt works on fresh copies, which is the undo. 

    stats["nodes"] = digits tried from a domain (counts faiiled attempts too, so it is close to, 
                but not identical to, the plain count)
    stats["wipeouts"] = dead ends caught by assign() before the search goes deeper  """

    cell = select_mrv_cell(grid, domain)
    if cell is None:
        return grid  # no blanks left: the grid itself is the solution
    row, col = cell
    for digit in domain[row][col]:
        # fresh copies per digit so a failed attempt leaves nothing behind
        grid_copy = copy.deepcopy(grid)
        domain_copy = copy.deepcopy(domain)
        # nodes = digits tried
        stats["nodes"] += 1
        if assign(grid_copy, domain_copy, row, col, digit):
            result = fc_search(grid_copy, domain_copy, stats)
            if result is not None:
                return result
        else:
            stats["wipeouts"] += 1
        # counted whether assign failed immediately or the deeper search failed
        stats["backtracks"] += 1
    return None     # every digit faiied, so the caller has to try a different


def conflict_check(grid):
    """ Return True if two given digits clash (e.g, two 5s in one row)
    The search only validates digits it places, so without this a puzzle with clashing givens 
    could be reported as solved. Each given is temporarily emptied so is_valid doesn't find
    it in its own cell, then put back.

    It is a helper function that performs pre-checks    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                digit = grid[row][col]
                grid[row][col] = 0      # empty the cell
                value_fit = is_valid(grid, row, col, digit)
                grid[row][col] = digit      # always restore, whatever the answer
                if not value_fit:
                    return True
    return False # no conflicts found


def solve(grid, mode="plain"):
    """ Solve a puzzle and then measure the search.
    grid: 9x9 list of ints (0 = blank). It is copied, so the caller's puzzle is never changed.
    mode: "plain: or "fc". Any other value raises ValueError.
    
    Returns (solution, stats):
    solution - solved 9x9 grid, or None if the puzzle has no solution 
    stats  - dictionary with nodes, backtracks, wipeouts *fc only, 0 for plain) and time in seconds   """
    
    valid_modes = ["plain", "fc"]
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode} Please choose 'plain' or 'fc'.")

    grid_copy = copy.deepcopy(grid)
    stats ={"nodes": 0, "backtracks": 0, "wipeouts": 0, "time": 0}

    # clashing givens: report no solution without searching (nodes stay 0)
    if conflict_check(grid_copy):
        stats["time"] = 0
        return None, stats

    # the timer covers the search only, but in fc mode it also covers 
    # compute_domains, a setup cost that plain mode does not pay
    start_time = time.perf_counter()
    if mode == "plain":
        # backtrack edits the copy in place and only returns True/False
        result = backtrack(grid_copy, stats)
        if result is True:
            answer = grid_copy
        else:
            answer = None
    else: # mode is "fc"
        domain = compute_domains(grid_copy)
        answer = fc_search(grid_copy, domain, stats)
    end_time = time.perf_counter()
    stats["time"] = end_time - start_time
    return answer, stats


# quick demo: both solvers on on epuzzle (run from the project root)
if __name__ == "__main__":
    grid = load_puzzle("puzzles/easy1.txt")
    plain_solution, plain_stats = solve(grid, "plain")
    fc_solution, fc_stats = solve(grid, "fc")

    print("Plain solution:")
    print_grid(plain_solution)
    print("plain stats:", plain_stats)
    print("fc stats:    ", fc_stats)
    print("Same answer from both?", plain_solution == fc_solution)