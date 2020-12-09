def search(mat, x):
    if (mat is None or len(mat) <= 0):
        return -1, -1
    if (len(mat) == 1 and 1 == len(mat[0])):
        return (0, 0) if mat[0][0] == x else (-1, -1)
    start = (0, 0)
    end = (len(mat), len(mat[0]))
    
    mid_row = (end[0] - start[0]) // 2
    mid_col = (end[1] - start[1]) // 2
    mid_val = mat[mid_row][mid_col]
    if mid_val == x:
        return mid_row, mid_col

    rows = [(0, mid_row if end[0] > 2 else 0), (mid_row, len(mat) - 1)]
    cols = [(0, mid_col if end[1] > 2 else 0), (mid_col, len(mat[0]) - 1)]
    
    if rows[0] == rows[1]:
        rows.pop()
    if cols[0] == cols[1]:
        cols.pop()

    quads = [(row, col) for row in rows for col in cols]
    if (len(quads) == 4):
        quads.pop(0 if mid_val < x else len(quads) - 1)
    
    for quad in quads:
        r = quad[0]
        c = quad[1]
        sub_mat = mat[r[0]:r[1] + 1]
        for i in range(len(sub_mat)):
            sub_mat[i] = sub_mat[i][c[0]:c[1] + 1]
        i, j = search(sub_mat, x)
        if i >= 0 and j >= 0:
            return r[0] + i, c[0] + j

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