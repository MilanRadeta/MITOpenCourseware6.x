def search(mat, x):
    if (mat is None or len(mat) <= 0):
        return -1, -1
    
    max_j = len(mat[0]) - 1
    for i in range(len(mat)):
        while max_j >= 0:
            val = mat[i][max_j]
            if val == x:
                return i, j
            if val < x:
                break
            max_j -= 1
    return -1, -1

T = [
    [1, 4, 7, 11, 15],
    [2, 5, 8, 12, 19],
    [3, 6, 9, 16, 22],
    [10, 13, 14, 17, 24],
    [18, 21, 23,26 ,30 ],
]

for i in range(len(T)):
    for j in range(len(T[i])):
        result = search(T, T[i][j])
        if result != (i, j):
            print('FAIL - expected: %s, actual %s' % ((i,j), result))