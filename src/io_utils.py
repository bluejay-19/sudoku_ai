""" Puzzle input and output helpers.

    load_puzzle reads and validates a puzzle file
    print_grid displays the sudoku grid 

    This module imports nothing from the rest of the project, so solver.py can import it 
    without the error of creating a circular import.

"""

""" Read a puzzle from a .txt(space-separated) or .csv(comma-separated) file 

    Returns a 9x9 list of integers, where 0 represnts a blank cell.
    Raisees ValueError, naming the line in the grid, if a row contains a non-nuumber, does 
    not have exactly 9 values, or has values outside 0-9. It also raises ValueError if the 
    file itself does not contai exactly 9 rows. 
    Additionally it also raises FileNotFoundError if the path does not exist (from open())

"""
def load_puzzle(path):
    # create an empty list to store the rows in our sudoku
    grid = []
    # open the file for reading
    with open(path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue    # skip blank lines, e.g. a trailing newline at the end of the file

            # turning commas into spaces lets on esplit() handle both expected file formats
            row = line.replace(',', ' ').split()

            # int() will fail on anything that is not a number, so convert the value first and report the line if failed
            try:
                row = [int(value) for value in row]
            except ValueError:
                raise ValueError(f"Line {line_number}: contains a non-integer value.")

            # check if the row has 9 values as expected
            if len(row) != 9:
                raise ValueError(f"Line {line_number}: expected 9 values in per row but found {len(row)}")

            # check that values in the row are in the correct range of accepted values
            if not all(0 <= value <= 9 for value in row):
                raise ValueError(f"Line {line_number}: values must be in between 0 and 9.")

            grid.append(row)

        # the row count can only be checked once the entire loaded file has been read 
        if len(grid) != 9:
            raise ValueError(f"Expected 9 rows in total instead got {len(grid)} rows.")

    return grid

""" Prints a 9x9 grid with separators between the 3x3 boxes: 0 is represted using dots '.'  """
def print_grid(grid):
    # row loop
    for row_index, row in enumerate(grid, start=0):
        grid_values = []
        # horizontal divider before the 2nd and 3rd band of boxes (not before the first row)
        if row_index % 3 == 0 and row_index != 0:
            print("------+-------+------")

        for col_index, value in enumerate(row, start=0):
            # vertical divider before the 2nd and 3rd box in each row
            if col_index % 3 == 0 and col_index != 0:
                grid_values.append("|")
            if value == 0:
                grid_values.append(".")
            else:
                grid_values.append(str(value))
        print(" ".join(grid_values))

# quick demo which only runs when this file is executed directly
if __name__ == "__main__":
    #print(load_puzzle("puzzles/bad.txt"))
    grid = load_puzzle("puzzles/easy1.txt")
    print_grid(grid)