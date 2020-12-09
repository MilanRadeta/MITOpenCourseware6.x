#Programming for the Puzzled -- Srini Devadas
#You Will Never Want to Play Sudoku Again
#Given a partially filled in Sudoku board, complete the puzzle
#obeying the rules of Sudoku
from inputs import all_inputs
from utils import sudoku_size, segment_size, findNextCellToFill, isValid, printSudoku

def getSectors():
    intervals = [(i, i + segment_size) for i in range(0, sudoku_size, segment_size)]
    return [[row[0], row[1], col[0], col[1]] for col in intervals for row in intervals]

#x varies from entry1 to entry2 - 1, y varies from entry3 to entry4 - 1 
sectors = getSectors()

def getSectorInfo(grid, sector):
    sectinfo = []

    #find missing elements in ith sector
    vset = set(range(1, sudoku_size + 1))
    for x in range(sector[0], sector[1]):
        for y in range(sector[2], sector[3]):
            if grid[x][y] != 0:
                vset.remove(grid[x][y])

    #attach copy of vset to each missing square in ith sector
    for x in range(sector[0], sector[1]):
        for y in range(sector[2], sector[3]):
            if grid[x][y] == 0:
                sectinfo.append([x, y, vset.copy()])
    
    return sectinfo

def findUsedValues(grid, coords):
    return set([grid[x][y] for x, y in coords])

#This procedure makes implications based on existing numbers on squares
def makeImplications(grid, i, j, e):
    impl = []
    if i >= 0 and j >= 0:
        grid[i][j] = e
        impl.append((i, j, e))

    easiest_cell = (-1, -1, None)
    made_changes = True
    while made_changes:
        easiest_cell = (-1, -1, None)
        made_changes = False
        for sector in sectors:

            sectinfo = getSectorInfo(grid, sector)

            for sin in sectinfo:
                #find the set of elements on the row/column corresponding to sin and remove them
                coords = [(sin[0],y) for y in range(sudoku_size)]
                coords.extend([(x,sin[1]) for x in range(sudoku_size)])
                usedVals = findUsedValues(grid, coords)
                left = sin[2].difference(usedVals)
                sin[2] = left
                            
                #check if the vset is a singleton
                if len(left) == 1:
                    made_changes = True
                    val = left.pop()
                    if isValid(grid, sin[0], sin[1], val):
                        grid[sin[0]][sin[1]] = val
                        impl.append((sin[0], sin[1], val))
                elif easiest_cell[2] is None or len(easiest_cell[2]) > len(left):
                    easiest_cell = sin

                
    return impl, easiest_cell

#This procedure undoes all the implications
def undoImplications(grid, impls):
    for imp in impls:
        grid[imp[0]][imp[1]] = 0
    return


#This procedure fills in the missing squares of a Sudoku puzzle
#obeying the Sudoku rules by guessing when it has to and performing
#implications when it can
def solveSudoku(grid, makeInitImplications=False, findNextCellByImpl=False, i=0, j=0, backtracks=0):
    initimpl = None
    next_cell = None
    if findNextCellByImpl:
        makeInitImplications = True

    if makeInitImplications:
        initimpl, next_cell = makeImplications(grid, -1, -1, 0)

    #find the next empty cell to fill
    if findNextCellByImpl:
        i, j, vals = next_cell
    else:
        i, j = findNextCellToFill(grid)
    if i == -1:
        return True, backtracks

    for e in range(sudoku_size):
        e += 1
        #Try different values in i, j location
        if isValid(grid, i, j, e):

            impl, sin = makeImplications(grid, i, j, e)
            
            solved, backtracks = solveSudoku(grid, makeInitImplications, findNextCellByImpl, i, j, backtracks)
            if solved:
                return True, backtracks
            #Undo the current cell for backtracking
            backtracks += 1
            undoImplications(grid, impl)

    if makeInitImplications:
        undoImplications(grid, initimpl)
    return False, backtracks

for inp in all_inputs:
    solved, backtracks = solveSudoku(inp, makeInitImplications=True, findNextCellByImpl=True)
    printSudoku(inp)
    print ('Backtracks = ', backtracks)
    print('-'*30)

