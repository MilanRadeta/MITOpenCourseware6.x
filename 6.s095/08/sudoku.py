#Programming for the Puzzled -- Srini Devadas
#You Will Never Want to Play Sudoku Again
#Given a partially filled in Sudoku board, complete the puzzle
#obeying the rules of Sudoku

sudoku_size = 9
segment_size = sudoku_size // 3

#This procedure finds the next empty square to fill on the Sudoku grid
def findNextCellToFill(grid):
    #Look for an unfilled grid location
    for x in range(sudoku_size):
        for y in range(sudoku_size):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def checkSegment(grid, i, j, e):
    #finding the top left x,y co-ordinates of
    #the section or sub-grid containing the i,j cell
    secTopX, secTopY = segment_size *(i//segment_size), segment_size *(j//segment_size)
    for x in range(secTopX, secTopX+segment_size):
        for y in range(secTopY, secTopY+segment_size):
            if grid[x][y] == e:
                return False
    return True

#This procedure checks if setting the (i, j) square to e is valid
def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            return checkSegment(grid, i, j, e)
    return False

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


def printSudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % segment_size == 0 and numrow != 0:
            print (' ')
        for i in range(0, sudoku_size, segment_size):
            print (row[i:i+segment_size], end='  ')
        print()
        numrow += 1       
    return

input = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

inp2  = [[5,1,7,6,0,0,0,3,4],
         [0,8,9,0,0,4,0,0,0],
         [3,0,6,2,0,5,0,9,0],
         [6,0,0,0,0,0,0,1,0],
         [0,3,0,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

inpd  = [[1,0,5,7,0,2,6,3,8],
         [2,0,0,0,0,6,0,0,5],
         [0,6,3,8,4,0,2,1,0],
         [0,5,9,2,0,1,3,8,0],
         [0,0,2,0,5,8,0,0,9],
         [7,1,0,0,3,0,5,0,2],
         [0,0,4,5,6,0,7,2,0],
         [5,0,0,0,0,4,0,6,3],
         [3,2,6,1,0,7,0,0,4]]

hard  = [[8,5,0,0,0,2,4,0,0],
         [7,2,0,0,0,0,0,0,9],
         [0,0,4,0,0,0,0,0,0],
         [0,0,0,1,0,7,0,0,2],
         [3,0,5,0,0,0,9,0,0],
         [0,4,0,0,0,0,0,0,0],
         [0,0,0,0,8,0,0,7,0],
         [0,1,7,0,0,0,0,0,0],
         [0,0,0,0,3,6,0,4,0]]

diff  = [[0,0,5,3,0,0,0,0,0],
         [8,0,0,0,0,0,0,2,0],
         [0,7,0,0,1,0,5,0,0],
         [4,0,0,0,0,5,3,0,0],
         [0,1,0,0,7,0,0,0,6],
         [0,0,3,2,0,0,0,8,0],
         [0,6,0,5,0,0,0,0,9],
         [0,0,4,0,0,0,0,3,0],
         [0,0,0,0,0,9,7,0,0]]


inps = [input, inp2, hard, diff]
for inp in inps:
    solved, backtracks = solveSudoku(inp)
    printSudoku(inp)
    print ('Backtracks = ', backtracks)
    print('-'*30)