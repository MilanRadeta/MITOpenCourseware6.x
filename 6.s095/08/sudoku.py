#Programming for the Puzzled -- Srini Devadas
#You Will Never Want to Play Sudoku Again
#Given a partially filled in Sudoku board, complete the puzzle
#obeying the rules of Sudoku
from inputs import all_inputs
from utils import sudoku_size, findNextCellToFill, isValid, printSudoku

#This procedure fills in the missing squares of a Sudoku puzzle
#obeying the Sudoku rules through brute-force guessing and checking
def solveSudoku(grid, i=0, j=0, backtracks=0):
    #find the next cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True, backtracks

    for e in range(sudoku_size):
        e += 1
        #Try different values in i, j location
        if isValid(grid, i, j, e):
            grid[i][j] = e
            solved, backtracks = solveSudoku(grid, i, j, backtracks)
            if solved:
                return True, backtracks
            
            #Undo the current cell for backtracking
            backtracks += 1
            grid[i][j] = 0

    return False, backtracks

for inp in all_inputs:
    solved, backtracks = solveSudoku(inp)
    printSudoku(inp)
    print ('Backtracks = ', backtracks)
    print('-'*30)