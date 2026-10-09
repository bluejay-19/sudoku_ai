def load_puzzle(path):
    # create an empty list to store the rows in our sudoku
    grid = []
    # open the file for reading
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            row = line.replace(',', ' ').split()
            row = [int(value) for value in row]
            grid.append(row)

    return grid

# file only run when called directly
if __name__ == "__main__":
    print(load_puzzle("puzzles/easy1.txt"))

# def print_grid(grid):
