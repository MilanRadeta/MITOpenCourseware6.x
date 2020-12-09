#Programming for the Puzzled -- Srini Devadas
#Tile that Courtyard, Please
#Given n in a 2^n x 2^n checkyard with a missing square at position (r, c), 
#find tiling of yard with trominoes (L-shaped dominoes).
#This version works directly on the given grid, and does NOT make copies
#of the grid for recursive calls.

import string

EMPTYPIECE = -1

diffs = [(0,0), (0,1), (1,0), (1,1)]

#This procedure is the main engine of recursive algorithm
#nextPiece is the number of next available tromino piece
#The origin coordinates of the yard are given by originR and originC
def recursiveTile(yard, size, originR, originC, rMiss, cMiss, nextPiece):

    #quadrant of missing square: 0 (upper left), 1 (upper right),
    #                            2 (lower left), 3 (lower right)
    quadMiss = 2*(rMiss >= size//2) + (cMiss >= size//2)

    #base case of 2x2 yard
    if size == 2: 
        piecePos = diffs.copy()
        piecePos.pop(quadMiss)
        for (r, c) in piecePos:
            yard[originR + r][originC + c] = nextPiece
        nextPiece = nextPiece + 1
        return nextPiece

    #recurse on each quadrant
    half_size = size // 2    
    for quad in range(4):
        #Each quadrant has a different origin
        #Quadrant 0 has origin (0, 0), Quadrant 1 has origin (0, size//2)
        #Quadrant 2 has origin (size//2, 0), Quadrant 3 has origin (size//2, size//2)
        shiftR = half_size * (quad >= 2)
        shiftC = half_size * (quad % 2 == 1)
        if quad == quadMiss:
            #Pass the new origin and the shifted rMiss and cMiss
            nextPiece = recursiveTile(yard, half_size, originR + shiftR,\
                originC + shiftC, rMiss - shiftR, cMiss - shiftC, nextPiece)

        else:
            #The missing square is different for each of the other 3 quadrants
            newrMiss = (half_size - 1) * (quad < 2)
            newcMiss = (half_size - 1) * (quad % 2 == 0)
            nextPiece = recursiveTile(yard, half_size, originR + shiftR,\
                            originC + shiftC, newrMiss, newcMiss, nextPiece)


    #place center tromino
    centerPos = [(r + half_size - 1, c + half_size - 1)
                 for (r,c) in diffs]
    centerPos.pop(quadMiss)
    for (r,c) in centerPos: # assign tile to 3 center squares
        yard[originR + r][originC + c] = nextPiece
    nextPiece = nextPiece + 1

    return nextPiece

#This procedure is a wrapper for recursiveTile that does all the work
def tileMissingYard(n, rMiss, cMiss):
    #Initialize yard, this is the only memory that will be modified!
    yard = [[EMPTYPIECE for i in range(2**n)]
            for j in range(2**n)] 
    recursiveTile(yard, 2**n, 0, 0, rMiss, cMiss, 0)
    return yard

ARROWS = ['←','↗','↓','↖','→','↙','↑','↘']
LETTERS = string.ascii_letters
UPPERS = string.ascii_uppercase
LOWERS = string.ascii_lowercase
XYZ = 'UWXYZ'
OPS = '!@#%^&*()_+-=[]:|<>"''\\/'
OPS2 = '+-[]<>|-"\\/'
SPECS = '|-\\/<>^v'

#This procedure prints a given tiled yard using letters for tiles
def printYard(yard, signs=SPECS, repeat=2, end=' '):
    size = len(signs)
    for i in range(len(yard)):
        for j in range(len(yard[0])):
            if yard[i][j] != EMPTYPIECE:
                print(('%s' % signs[yard[i][j] % size]) * repeat, end=end)
            else:
                print('?' * repeat, end=end)
        print()
    print()


def canTile(size, missingTiles):
    size = 2 ** size
    half_size = size // 2
    quads = list(range(4))
    for tile in missingTiles:
        quad = 2*(tile[0] >= half_size) + (tile[1] >= half_size)
        if quad not in quads:
            break
        quads.remove(quad)

    if len(quads) == 0:
        return True

    for tile in missingTiles:
        tile_diffs = [(0, 1), (1, 0)]
        for other in missingTiles:
            if tile != other:
                diff = (abs(tile[0] - other[0]), abs(tile[1] - other[1]))
                if diff in tile_diffs:
                    tile_diffs.remove(diff)
        if len(tile_diffs) == 0:
            return True

    return False
    


# printYard(tileMissingYard(3, 4, 6))
# printYard(tileMissingYard(4, 5, 7))

print(canTile(3, [(4, 4), (1, 1), (4, 1), (1, 4)]))
print(canTile(3, [(4, 4), (3, 1), (2, 1), (1, 2)]))
print(canTile(3, [(3, 7), (4, 4), (4, 6), (4, 7)]))