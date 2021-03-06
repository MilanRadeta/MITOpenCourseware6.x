#Programming for the Puzzled -- Srini Devadas
#You Will Never Want to Play Sudoku Again
#Given a partially filled in Sudoku board, complete the puzzle
#obeying the rules of Sudoku
from inputs import inpd, even, getInputs
from utils import sudoku_size, getSectors, findNextCellToFill, isValid, printSudoku

#x varies from entry1 to entry2 - 1, y varies from entry3 to entry4 - 1 
sectors = getSectors()

def getSectorInfo(grid, sector):
    sectinfo = []

    #find missing elements in ith sector
    vset = set(range(1, sudoku_size + 1))
    for x in range(sector[0], sector[1]):
        for y in range(sector[2], sector[3]):
            if grid[x][y] > 0:
                vset.remove(grid[x][y])

    #attach copy of vset to each missing square in ith sector
    for x in range(sector[0], sector[1]):
        for y in range(sector[2], sector[3]):
            if grid[x][y] == 0:
                sectinfo.append([x, y, vset.copy()])
            elif grid[x][y] == -2:
                sectinfo.append([x, y, {v for v in vset if v % 2 == 0}])
    
    return sectinfo

def findUsedValues(grid, coords):
    return {grid[x][y] for x, y in coords if grid[x][y] > 0}

#This procedure makes implications based on existing numbers on squares
def makeImplications(grid, i, j, e, checkDiags=False):
    impl = []
    if i >= 0 and j >= 0:
        impl.append((i, j, grid[i][j]))
        grid[i][j] = e

    i, j = findNextCellToFill(grid)
    easiest_cell = (i, j, None)
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
                if checkDiags:
                    if sin[0] == sin[1]:
                        coords.extend([(i, i) for i in range(sudoku_size)])
                    if sin[0] == sudoku_size - sin[1] - 1:
                        coords.extend([(i, sudoku_size - i - 1) for i in range(sudoku_size)])

                usedVals = findUsedValues(grid, coords)
                left = sin[2].difference(usedVals)
                sin[2] = left
                            
                #check if the vset is a singleton
                if len(left) == 1:
                    made_changes = True
                    val = left.pop()
                    impl.append((sin[0], sin[1], grid[sin[0]][sin[1]]))
                    grid[sin[0]][sin[1]] = val
                    
                    for other in sectinfo:
                        if val in other[2]:
                            other[2].remove(val)
                            if len(other[2]) == 0:
                                return impl, other

                elif easiest_cell[2] is None or len(easiest_cell[2]) > len(left):
                    easiest_cell = sin

                
    return impl, easiest_cell

#This procedure undoes all the implications
def undoImplications(grid, impls):
    for imp in impls:
        grid[imp[0]][imp[1]] = imp[2]
    return


#This procedure fills in the missing squares of a Sudoku puzzle
#obeying the Sudoku rules by guessing when it has to and performing
#implications when it can
def solveSudoku(grid, i=-1, j=-1, e=0, backtracks=0, checkDiags=False):
    initimpl, next_cell = makeImplications(grid, i, j, e, checkDiags=checkDiags)
    
    #find the next empty cell to fill
    i, j, vals = next_cell
    
    if i == -1:
        return True, backtracks

    for e in range(sudoku_size):
        e += 1
        if grid[i][j] == -2 and e % 2 == 1:
            continue

        #Try different values in i, j location
        if isValid(grid, i, j, e, checkDiags=checkDiags):

            solved, backtracks = solveSudoku(
                grid, i=i, j=j, e=e, backtracks=backtracks,
                checkDiags=checkDiags)
            if solved:
                return True, backtracks
            #Undo the current cell for backtracking
            backtracks += 1

    undoImplications(grid, initimpl)
    return False, backtracks

print('Default strategy')
for inp in getInputs():
    inp = inp.copy()
    solved, backtracks = solveSudoku(inp)
    printSudoku(inp)
    print ('Backtracks = ', backtracks)
    print('-'*30)

print('Diagonal Sudoku')
test = getInputs([inpd])[0]
solved, backtracks = solveSudoku(test, checkDiags=True)
printSudoku(test)
print ('Backtracks = ', backtracks)
print('-'*30)

print('Even Sudoku')
test = getInputs([even])[0]
solved, backtracks = solveSudoku(test)
printSudoku(test)
print ('Backtracks = ', backtracks)
print('-'*30)
