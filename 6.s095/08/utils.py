
sudoku_size = 9
segment_size = sudoku_size // 3


def getSectors():
    intervals = [(i, i + segment_size) for i in range(0, sudoku_size, segment_size)]
    return [[row[0], row[1], col[0], col[1]] for col in intervals for row in intervals]
    
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
def isValid(grid, i, j, e, checkDiags=False):
    rowOk = all([e != grid[i][x] for x in range(sudoku_size)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(sudoku_size)])
        if columnOk:
            if checkSegment(grid, i, j, e):
                if checkDiags:
                    if i == j:
                        diagonalOk1 = all([e != grid[x][x] for x in range(sudoku_size)])
                        if not diagonalOk1:
                            return False
                    if i == sudoku_size - j - 1:
                        diagonalOk2 = all([e != grid[x][sudoku_size - x - 1] for x in range(sudoku_size)])
                        if not diagonalOk2:
                            return False
                return True
    return False


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