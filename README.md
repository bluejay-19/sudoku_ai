This is an intelligent version of a sudoku solver that incorporates the concept of plain backtracking as well as heueristic search of Minimum vValue Remaining as well as Forward Checking 

There are several tests files obtained from https://sudokly.com/hardest-sudoku/
From this website used the easy, medium, hard and expert puzzle examples available for testing the solver.
In addition to that there is a file named brute-force.txt which is used to test the brute force capability of the solver 

There is also a results folder which contains two csv files that contain the necessary statistics run on the test puzzles. One is just for all the puzzles ranging from easy 1 to expert1 and then other is specifically for the brute force test

The src folder contains all the code for the solver including the main solving logic, the benchmark code for testing and retrieving stats, the utility functions and finally a file for the graphical user interace(GUI - the visual aspect of the solver).
