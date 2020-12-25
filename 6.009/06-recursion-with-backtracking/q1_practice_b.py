def vals_at_depth(tree, depth):
    if depth == 0:
        return [tree[0]]
    if len(tree) == 1:
        return []
    return [val for subtree in tree[1:] for val in vals_at_depth(subtree, depth - 1)]

tree2 = [7,
          [3,
            [4],
            [1,
              [7]],
            [2]],
          [8,
            [1]]]

assert vals_at_depth(tree2, 0) == [7]
assert vals_at_depth(tree2, 1) == [3, 8] or [8, 3]
assert vals_at_depth(tree2, 2) ==  [4, 1, 2, 1]
assert vals_at_depth(tree2, 3) == [7]
assert vals_at_depth(tree2, 4) == []
assert vals_at_depth([], 4) == []

def weave(list1, list2):
    pointers = { 'list1': 0, 'list2': 0 }
    lists = { 'list1': list1, 'list2': list2 }
    key = 'list1'
    res = []
    while len(lists) > 0:
        val = lists[key][pointers[key]]
        pointers[key] += 1

        if pointers[key] >= len(lists[key]):
            del lists[key]
            if len(lists) > 0:
                key = list(lists.keys())[0]
        
        if len(res) == 0 or val != res[-1]:
            if len(lists) == 2:
                key = (lists.keys() - {key}).pop()
            res.append(val)

    return res

assert weave(['a', 'b'], ['b', 'c']) == ['a', 'b', 'c']
assert weave(['a', 'b'], ['a', 'c']) == ['a', 'c', 'b']
assert weave(['a', 'b', 'd'], ['a', 'c']) == ['a', 'c', 'b', 'd']
assert weave(['a', 'a', 'a', 'a', 'a'], ['b']) == ['a', 'b', 'a']

def all_blobs(world):
    nrows = world['nrows']
    ncols = world['ncols']
    grid = world['grid']
    indexes = {(i, j) for j in range(ncols) for i in range(nrows) if grid[i][j] is not None}
    diffs = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    res = []
    while len(indexes) > 0:
        i, j = indexes.pop()
        val = grid[i][j]
        blob = {(i,j)}
        elem = [val, blob]
        neighbours = {(i,j)}
        while len(neighbours) > 0:
            blob |= neighbours
            indexes -= neighbours
            neighbours = indexes & {(i+di, j+dj) for di, dj in diffs for i, j in neighbours
                                    if 0 <= i+di < nrows and 0 <= j+dj < ncols and grid[i+di][j+dj] == val}
        res.append(elem)
    return res

world1 = {
    "nrows": 5,
    "ncols": 6,
    "grid": [[None, None, 'G', None, 'R', None],
            ['R', 'R', 'R', 'R', None, None],
            [None, None, None, 'R', None, None],
            ['B', 'B', None, 'G', 'G', 'G'],
            ['B', 'B', None, None, None, None]]}


for elem in all_blobs(world1):
    assert elem in [['G', {(0, 2)}], ['R', {(0, 4)}], ['R', {(1, 2), (1, 0), (1, 3), (2, 3), (1, 1)}], ['B', {(3, 0), (3, 1), (4, 1), (4, 0)}], ['G', {(3, 4), (3, 3), (3, 5)}]]
assert all_blobs({"nrows": 1, "ncols": 1, "grid": [[None]]}) == []
