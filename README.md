#  Sudoku Solver 
This is an intelligent version of a sudoku solver that incorporates the concept of plain backtracking paired with MRV(Minimum Remaining Values) and forward checking.

## Features 
- Plain Backtracking 
- MRV + FC (Minimum Remaining Values + Forwarrd Checkimg) 
- GUI (tkinter)
- Command-line mode 
- Benchmark script 
- .txt and .csv input 

## Requirements & Tech Stack
- Python 3.13
- tkinter (GUI)
- Standard built-in libraries: os, copy, time, csv, sys
- matplotlib - for chart visualisation

---

## How to run: 
Run all commands from the project root
``` 
python src/gui.py
python src/main.py puzzles/easy1.txt [plain|fc] (default = fc) 
python src/benchmark.py

pip install -r requirements.txt
python src/make_charts.py

```

---

## Project Structure 
```
sudoku_ai/
├── src/
│   ├── benchmark.py              # runs both modes on the puzzles, writes results/results.csv
│   ├── benchmark_bruteforce.py   # separate run for the very slow brute-force puzzle
│   ├── gui.py                    # tkinter window
│   ├── io_utils.py               # loading and validating puzzles
│   ├── main.py                   # command-line entry point
│   ├── make_charts.py            # draws the evaluation charts (needs matplotlib)
│   └── solver.py                 # validity checks, plain backtracking, MRV, forward checking
├── puzzles/                      # test puzzles (easy, medium, hard, expert, bad, unsolvable, csv example)
├── results/                      # benchmark output and charts
├── README.md
├── requirements.txt
└── .gitignore

```
---

## Puzzles 
File format: 9 lines of 9 values whhich are either separted by spaces for ```.txt``` files or by commas for ```.csv``` files. 0's in the file represent blank/empty cells

```bad.txt ``` is the file that contains clashing givens - duplicate in a row/column/box, rejected before search  

```unsolvable1.txt``` givens are consistent but no solution exists, search fails immediately

---

## Known limitations 
The GUI does freeze when a very long solve (e,g the brute-force puzzle) in plain mode typically takes about 10 minutes. Hence the test showing the results of solving the brute-force puzzle is done in its own separate file ```benchmark_bruteforce.py``` and ```results/brute-force.csv```

---

## References 
- All puzzles used for testing were obtained from this link: https://sudokly.com/hardest-sudoku/
- The brute force puzzle was taken from the Wikipedia page on Sudoku solving algorithms: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms