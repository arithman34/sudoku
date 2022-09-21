# Sudoku
Implementation of the sudoku problem in python's pygame library

### Motivation
This project was inspired by initially attempting to solve a sudoku puzzle while on a treadmill. This failed miserablly. So like any other programmer I coded a sudoku solver (may have also needed to learn how sudoku is solved too). Further versions of the project then included the puzzle, where cells are removed and difficulties are set for the generated puzzle. A lot of the ideas in the design aspect was inspired by the use of Android Studio in my internship.

### Build Status
Further testing on the threading aspect is needed. However, in generally the code performs well without bugs (i think).
Some variables might also be redundant. And further optimisation of several methods or functions need to be carried out.

### Possible iterations
* Adding different solving methods rather than backtracking (using brute force). One idea could be a human version. Where naturally we identify cells with the least possible numbers and attempt to solve them first.

### Choices
A lot of what has been coded can be replicated far more simply by hard-coding values. Take the table class. In many of these cases, this slightly costly method was introduced to allow for changes. The container class can format different views.
