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
    
def NQueens(n = 8, maxSolutions = None):
    result = []
    board = [-1] * n
    col = 0
    solutions_count = 0
    while col >= 0:
        board[col] += 1
        if board[col] >= n:
            board[col] = -1
            col -= 1
            continue
        
        if noConflicts(board, col):
            if col == n - 1:
                print(board)
                # printBoard(board, n)
                result.append(board.copy())
                solutions_count += 1
                if maxSolutions is not None and solutions_count >= maxSolutions:
                    return result
            else:
                col += 1
    return result
                

def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print('0' if board[j] != i else '1', end=' ')
        print()
    print()

# NQueens(5)
NQueens(8, 3)
