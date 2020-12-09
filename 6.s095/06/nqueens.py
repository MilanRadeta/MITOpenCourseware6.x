#Programming for the Puzzled -- Srini Devadas
#A Profusion of Queens
#Given the dimension of a square "chess" board, call it N, find a placement
#of N queens such that no two Queens attack each other using recursive search

#This procedure initializes the board to be empty, calls the recursive N-queens
#procedure and prints the returned solution
def nQueens(size, locations = None):
    board = [-1] * size
    rQueens(board, 0, size, locations)
    printBoard (board)

#This procedure checks that the most recently placed queen on column current
#does not conflict with queens in columns to the left.
def noConflicts(board, current):
    for i in range(current):
        if (board[i] == board[current]):
            return False
        if (current - i == abs(board[current] - board[i])):
            return False
    return True 


#This procedure places a queens on the board on a given column so it does
#not conflict with the existing queens, and then calls itself recursively
#to place subsequent queens till the requisite number of queens are placed
def rQueens(board, current, size, locations):
    if (current == size):
        return True
    else:
        arr = range(size)

        if locations is not None and locations[current] >= 0:
            arr = [locations[current]]
            
        for i in arr:
            board[current] = i
            if (noConflicts(board, current)):
                done = rQueens(board, current + 1, size, locations)
                if (done):
                    return True
    return False
  

def printBoard(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            print('.' if board[j] != i else 'Q', end=' ')
        print()
    print()

# nQueens(20)
nQueens(10, [-1, -1, 4, -1, -1, -1, -1, 0, -1, 5])
