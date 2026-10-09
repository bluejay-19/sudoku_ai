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
