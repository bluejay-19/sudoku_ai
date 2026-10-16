#  Sudoku Solver 
This is an intelligent version of a sudoku solver that incorporates the concept of plain backtracking paired with MRV(Minimum Value Remaining) and forward checking.

## Features 
- Plain Backtracking 
- Plain and MRV + FC modes 
- GUI (tkinter)
- Command-line mode 
- Benchmark script 
- .txt and .csv input 

## Requirements 
- Python version 
Both the python solver and the GUI use python's standard library that is shipped with tkinter
- matplotlib - for chart visualisation

---

## Tech Stack
- Python 3.13 
- tkinter (GUI)
- Standard built-in libraries: os, copy, time, csv, sys
- matplotlib 

---

## How to run: 
- command line: ``` python src/main.py puzzles/easy1.txt [plain|fc] (default =fc) ```
- GUI: ```python src/gui.py```
- benchmark: ```python src/benchmark.py``` then ```python src/make_charts.py```

---

## Project Structure 
```
sudoku_ai/
├── src/                      
|   └──benchmark.py             # runs both modes on the puzzles and writes to results/resuults.csv  
|   └──benchmark_bruteforce.py                        
|   └──gui.py                     # tkinter window   
|   └──io_utils.py                # loading and validating puzzles 
|   └──main.py                   # command-line entry point     
|   └──make_charts.py                        
|   └──solver.py        #solver logic - validity checks, plain backtracking, MRV, forward checking
│
├── puzzles/        # test puzzles
|   └──bad.txt
|   └──brute-force.txt
│   └──easy1.txt
|   └──easy2.txt
|   └──easy4.csv              
│   └──expert1.txt
|   └──expert2.txt
|   └──hard1.txt
|   └──hard2.txt
|   └──medium1.txt
|   └──medium2.txt
|   └──unsolvable1.txt
|
├── results/        # benchmark output
|   └──brute-force.csv
|   └──nodes_chart.png
|   └──results.csv
|   └──time_chart.png
|
└──README.md
└──requirements.txt
└──.gitignore

```
---

## Puzzles 
File format: 9 lines of 9 values whhich are either separted by spaces for ```.txt``` files or by commas for ```.csv``` files. 0's in the file represent blank/empty cells

---

## Known limitations 
The GUI does freeze when a very long solve (e,g the brute-force puzzle) in plain mode typically takes about 10 minutes. Hence the test showing the results of solving the brute-force puzzle is done in its own separate file ```benchmark_bruteforce.py``` and ```results/brute-force.csv```

---

## References 
- All puzzles used for testing were obtained from this link: https://sudokly.com/hardest-sudoku/
- The brute force puzzle was taken from the Wikipedia page on Sudoku solving algorithms: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms