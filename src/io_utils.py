def load_puzzle(path):
    # create an empty list to store the rows in our sudoku
    grid = []
    # open the file for reading
    with open(path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            row = line.replace(',', ' ').split()

            # safety check in case any value is not an integer
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

        # check if the grid has 9 rows
        if len(grid) != 9:
            raise ValueError(f"Expected 9 rows in total instead got {len(grid)} rows.")

    return grid

# file only run when called directly
if __name__ == "__main__":
    print(load_puzzle("puzzles/bad.txt"))

# def print_grid(grid):
