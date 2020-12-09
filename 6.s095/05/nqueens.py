#Programming for the Puzzled -- Srini Devadas
#Keep Those Queens Apart
#Given a 8 x 8 chess board, figure out how to place 8 Queens such that
#no Queen attacks another queen.
#This code uses a single-dimensional list to represent Queen positions


#This procedure checks that the most recently placed queen on the board on column
#current does not conflict with existing queens.
def noConflicts(board, current):
    for i in range(current):
        if (board[i] == board[current]):
            return False
        #We have two diagonals hence need the abs()
        if (current - i == abs(board[current] - board[i])):
            return False
    return True 
    
def NQueens(n = 8, maxSolutions = None, locations = None):

    result = []
    board = [-1] * n
    col = 0
    solutions_count = 0

    if locations is None or len(locations) == 0:
        locations = None
        
    if locations is not None:
        locations = locations.copy()
        while len(locations) < n:
            locations.append(0)
            
        while(col < n):
            board[col] = locations[col]
            col += 1
        col = 0

    col_diff = 1
    while col >= 0:
        skip_column = locations is not None and locations[col] >= 0
        if not skip_column:
            board[col] += 1
            col_diff = 1

            if board[col] >= n:
                board[col] = -1
                col_diff = -1
                col += col_diff
                continue

        if noConflicts(board, col):
            if col == n - 1:
                print(board)
                # printBoard(board, n)
                result.append(board.copy())
                solutions_count += 1
                if maxSolutions is not None and solutions_count >= maxSolutions:
                    break
                if skip_column:
                    col_diff = -1
                    col += col_diff
            else:
                col += col_diff
        elif skip_column:
            col_diff = -1
            col += col_diff
        
    print()
    return result
                

def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print('0' if board[j] != i else '1', end=' ')
        print()
    print()

# NQueens(n=4)
# NQueens()
# NQueens(maxSolutions=3)
NQueens(locations=[-1, 4, -1, -1, -1, -1, -1, 0])