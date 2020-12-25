def batch(inp, size):
    """
    Inputs:
      inp is a tuple of non-negative integers.
      size is a non-negative integer.

    Outputs:

    Return a list of batches, where each batch is a list of elements
    (in order from the beginning) from "inp", until the batch is
    populated with just enough elements to fill the batch. A batch
    is filled when the sum of the values of the elements in the
    batch is equal to or greater than "size", or if there are no more
    elements from "inp".

    >>> batch((13, 2, 3, 4, 3, 1, 1, 1, 4, 2, 3), 5)
    [[13], [2, 3], [4, 3], [1, 1, 1, 4], [2, 3]]

    >>> batch((6, 7, 6, 8, 6), 7)
    [[6, 7], [6, 8], [6]]

    """
    res = []
    start = 0
    sum = 0
    for i in range(len(inp)):
        elem = inp[i]
        sum += elem
        if sum >= size or i == len(inp) - 1:
            res.append(list(inp[start : i + 1]))
            start = i + 1
            sum = 0
    return res

def order(inp):
    """
    >>> order(['hi', 'yes', 'hello', 'yay'])
    ['hi', 'hello', 'yes', 'yay']
    >>> order(['yes', 'hi', 'yay', 'hello'])
    ['yes', 'yay', 'hi', 'hello']
    >>> order(['b', 'ab', 'doh', 'aa', 'c', 'aa'])
    ['b', 'ab', 'aa', 'aa', 'doh', 'c']
    """
    first_letters = [elem[0] for elem in inp]
    return sorted(inp, key=lambda e: first_letters.index(e[0]))


def path_to_happiness(field):
    """
    >>> path_to_happiness({"nrows": 2, "ncols": 3, "smiles": ((100, 3, 5), (2, 4, 6))})
    [0, 1, 1]
    >>> path_to_happiness({"nrows": 3, "ncols": 2, "smiles": ((6, 25), (5, 2), (4, 35))})
    [1, 2]
    >>> path_to_happiness({"nrows": 3, "ncols": 2, "smiles": ((5, 18), (6, 0), (4, 18))})
    [1, 2]
    """
    rows = field['nrows']
    cols = field['ncols']
    grid = field['smiles']

    agenda = [((i, 0), [i], grid[i][0]) for i in range(rows)]
    max_cost = None
    best_path = None

    while len(agenda) > 0:
        pos, path, cost = agenda.pop()
        row, col = pos
        if col == cols - 1:
            if (max_cost is None or max_cost < cost):
                max_cost = cost
                best_path = path
            continue

        for diff in range(-1, 2):
            pos = (row + diff, col + 1)
            x, y = pos
            if 0 <= x < rows:
                agenda.append((pos, path + [x], cost + grid[x][y]))

    return best_path




if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests