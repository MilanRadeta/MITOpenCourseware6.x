import time
from inputs import all_inputs

def format_sudoku(board):
    """
    Format a sudoku board to be printed to the screen
    """
    _divider = '+'+''.join('-+' if i%3==2 else '-' for i in range(9))
    lines = []
    for i in range(9):
        if i % 3 == 0:
            lines.append(_divider)
        line = '|'
        for j in range(9):
            line += ' ' if board[i][j] == 0 else str(board[i][j])
            if j % 3 == 2:
                line += '|'
        lines.append(line)
    lines.append(_divider)
    return '\n'.join(lines)


def values_in_row(board, r):
    """
    Return a set containing all of the values in a given row.
    """
    return board[r]


def values_in_column(board, c):
    """
    Return a list containing all of the values in a given column.
    """
    return [board[r][c] for r in range(len(board))]


def values_in_subgrid(board, sr, sc):
    """
    Return a list containing all of the values in a given subgrid.
    """
    return [board[r][c]
            for r in range(sr*3, (sr+1)*3)
            for c in range(sc*3, (sc+1)*3)]

def solve_sudoku(board, backtracks=0):
    """
    Given a sudoku board (as a list-of-lists of numbers, where 0 represents an
    empty square), return a solved version of the puzzle.
    """
    board = [row.copy() for row in board]

    all_candidates = {}

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                candidates = set(values_in_row(board, row))
                candidates |= set(values_in_column(board, col))
                candidates |= set(values_in_subgrid(board, row // 3, col // 3))
                candidates = set(range(1, 10)) - candidates
                if len(candidates) == 0:
                    return None, backtracks
                elif len(candidates) == 1:
                    board[row][col] = candidates.pop()
                else:
                    all_candidates[(row, col)] = candidates
    
    if len(all_candidates) == 0:
        return board, backtracks

    min_len = 10
    min_key = None
    for key in all_candidates:
        candidates = all_candidates[key]
        if min_len > len(candidates):
            min_len = len(candidates)
            min_key = key

    row, col = min_key
    candidates = all_candidates[(row, col)]
    for val in candidates:
        board[row][col] = val
        res, backtracks = solve_sudoku(board, backtracks)
        if res is not None:
            return res, backtracks
        backtracks +=1
    return None, backtracks
    


grid1 = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

grid2 = [[5,1,7,6,0,0,0,3,4],
         [0,8,9,0,0,4,0,0,0],
         [3,0,6,2,0,5,0,9,0],
         [6,0,0,0,0,0,0,1,0],
         [0,3,0,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

grid3 = [[0,0,1,0,0,9,0,0,3],  # http://www.extremesudoku.info/sudoku.html
         [0,8,0,0,2,0,0,9,0],
         [9,0,0,1,0,0,8,0,0],
         [1,0,0,5,0,0,4,0,0],
         [0,7,0,0,3,0,0,5,0],
         [0,0,6,0,0,4,0,0,7],
         [0,0,8,0,0,5,0,0,6],
         [0,3,0,0,7,0,0,4,0],
         [2,0,0,3,0,0,9,0,0]]

for grid in [grid1, grid2, grid3] + all_inputs:
    print(format_sudoku(grid))
    t = time.time()
    res, backtracks = solve_sudoku(grid)
    elapsed = time.time() - t
    print(format_sudoku(res))
    print(elapsed, 'seconds')
    print(backtracks, 'backtracks')
    print()