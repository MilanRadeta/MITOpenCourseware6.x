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
    
def NQueens(n = 8):
    result = []
    board = [-1] * n
    col = 0
    while col >= 0:
        board[col] += 1
        if board[col] >= n:
            board[col] = -1
            col -= 1
            continue
        
        if noConflicts(board, col):
            if col == n - 1:
                print(board)
                printBoard(board, n)
                result.append(board.copy())
            else:
                col += 1
    return result
                

def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print('0' if board[j] != i else '1', end=' ')
        print()
    print()


#This procedure places 8 Queens on a board so they don't conflict.
#It assumes n = 8 and won't work with other n!
def EightQueens(n=8):
    result = []
    board = [-1] * n
    for i in range(n):
        board[0] = i
        for j in range(n):
            board[1] = j
            if not noConflicts(board, 1):
                continue
            for k in range(n):
                board[2] = k
                if not noConflicts(board, 2):
                    continue
                for l in range(n):
                    board[3] = l
                    if not noConflicts(board, 3):
                        continue
                    for m in range(n):
                        board[4] = m
                        if not noConflicts(board, 4):
                            continue
                        for o in range(n):
                            board[5] = o
                            if not noConflicts(board, 5):
                                continue
                            for p in range(n):
                                board[6] = p
                                if not noConflicts(board, 6):
                                    continue
                                for q in range(n):
                                    board[7] = q
                                    if noConflicts(board, 7):
                                        print (board)
                                        result.append(board.copy())
    
    return result

# EightQueens()
NQueens(8)
# print(EightQueens() == NQueens(8))
