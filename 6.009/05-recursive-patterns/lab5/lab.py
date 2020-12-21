#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)

def new_nd_list(dimensions, val=0):
    """
    Creates an n-dimensional array recursively.
    
    Parameters:
        dimensions (tuple): Tuple of ints, representing each dimension size
        val (any): Default value for cells

    Returns:
        Return an n-dimensional list.

    >>> new_nd_list((3,2), 5)
    [[5, 5], [5, 5], [5, 5]]

    >>> new_nd_list((4,3,2), '1')
    [[['1', '1'], ['1', '1'], ['1', '1']], [['1', '1'], ['1', '1'], ['1', '1']], [['1', '1'], ['1', '1'], ['1', '1']], [['1', '1'], ['1', '1'], ['1', '1']]]
    """
    if len(dimensions) == 0:
        return val

    dim = dimensions[0]
    return [new_nd_list(dimensions[1:], val) for i in range(dim)]

def new_nd_diffs(n):
    """
    Parameters:
        n (int): Number of dimensions

    Returns:
        Returns a tuple of 3**n tuples of n diff values ranging from -1 to 1.

    >>> new_nd_diffs(1)
    ((-1,), (0,), (1,))

    >>> new_nd_diffs(2)
    ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))

    >>> new_nd_diffs(3)
    ((-1, -1, -1), (-1, -1, 0), (-1, -1, 1), (-1, 0, -1), (-1, 0, 0), (-1, 0, 1), (-1, 1, -1), (-1, 1, 0), (-1, 1, 1), (0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 0, -1), (0, 0, 0), (0, 0, 1), (0, 1, -1), (0, 1, 0), (0, 1, 1), (1, -1, -1), (1, -1, 0), (1, -1, 1), (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 1, -1), (1, 1, 0), (1, 1, 1))
    """

    if n == 0:
        return []
    base_diffs = tuple((i,) for i in range(-1, 2))
    if n == 1:
        return base_diffs
    
    diffs = []
    subdiffs = new_nd_diffs(n-1)
    for diff in base_diffs:
        for subdiff in subdiffs:
            diffs.append(diff + subdiff)
    return tuple(diffs)

def get_surrounding_indexes(index):
    """
    Get tuple of indexes surrounding provided index
    by adding values of index with values of diffs provided by new_nd_diffs.

    Each index is also an n-tuple of ints.

    Parameters:
        index (tuple): n-tuple of ints

    Returns:
        Returns a tuple of 3**n tuples of indexes surrounding the provided index and the provided index itself.

    >>> get_surrounding_indexes((0,))
    ((-1,), (1,))

    >>> get_surrounding_indexes((3,))
    ((2,), (4,))

    >>> get_surrounding_indexes((0,0))
    ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    >>> get_surrounding_indexes((2,2))
    ((1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3))

    >>> get_surrounding_indexes((1, 4, 8))
    ((0, 3, 7), (0, 3, 8), (0, 3, 9), (0, 4, 7), (0, 4, 8), (0, 4, 9), (0, 5, 7), (0, 5, 8), (0, 5, 9), (1, 3, 7), (1, 3, 8), (1, 3, 9), (1, 4, 7), (1, 4, 9), (1, 5, 7), (1, 5, 8), (1, 5, 9), (2, 3, 7), (2, 3, 8), (2, 3, 9), (2, 4, 7), (2, 4, 8), (2, 4, 9), (2, 5, 7), (2, 5, 8), (2, 5, 9))
    """
    diffs = new_nd_diffs(len(index))
    result = []
    for pair in zip((index,) * len(diffs), diffs):
        neighbour = tuple(map(sum, zip(*pair)))
        if neighbour != index:
            result.append(neighbour)
    return tuple(result)

def get_innermost_list(board, index):
    """
    Given the n-dimensional board and n-tuple index,
    return the innermost list according to the specified index
    along with last element from index.

    Dimension of the board and size of index must be equal.

    Parameters:
        board (list): n-dimensional list
        index (tuple): tuple with n values

    Returns:
        Returns a tuple (innermost_list, index[-1]) if index is valid, otherwise (None, None)

    >>> get_innermost_list([[1, 2], [3, 4]], (1, 0))
    ([3, 4], 0)
    >>> get_innermost_list([[1, 2], [3, 4]], (-1, 2))
    (None, None)
    >>> get_innermost_list([[1, 2], [3, 4]], (-1, -1))
    (None, None)
    """
    inner = board
    for i in index[:-1]:
        if i < 0 or i >= len(inner):
            return None, None
        inner = inner[i]
    i = index[-1]
    if i < 0 or i >= len(inner):
        return None, None
    return inner, i

def set_value(board, index, val):
    """
    Set the value at a specified n-tuple index in n-dimensional list.

    Dimension of the list and size of index must be equal.

    Parameters:
        board (list): n-dimensional list
        index (tuple): tuple with n values
        val (any): value to set or a setter function which receives current value as parameter and returns new value

    Returns:
        None
    """
    cell, i = get_innermost_list(board, index)
    if cell is not None:
        cell[i] = val(cell[i]) if callable(val) else val

def get_value(board, index):
    """
    Get the value at a specified n-tuple index in n-dimensional list.

    Dimension of the list and size of index must be equal.

    Parameters:
        board (list): n-dimensional list
        index (tuple): tuple with n values

    Returns:
        value (any): value at a given index
    >>> get_value([[1, 2], [3, 4]], (1, 0))
    3
    >>> get_value([[1, 2], [3, 4]], (-1, 2)) is None
    True
    >>> get_value([[1, 2], [3, 4]], (-1, -1)) is None
    True
    """
    cell, i = get_innermost_list(board, index)
    return None if cell is None else cell[i]

# 2-D IMPLEMENTATION

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game model dictionary with following properties:
    'dimensions' - tuple with value of (num_rows, num_cols)
    'state' - string, one of following values ('ongoing', 'victory', 'defeat')
    'board' - 2-dimensional array, with cell values of 0-8 (number of neighbour bombs) or '.' (bomb)
    'mask' - 2-dimensional array with boolean cell values, indicating which cells are revealed
    'bombs' - number of bombs
    'covered' -  number of covered cells
    'revealed' - number of revealed cells
    'total' - total number of cells
    
    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game object dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    covered: 8
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    revealed: 0
    state: ongoing
    total: 8
    """
    return new_game_nd((num_rows, num_cols), bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col) and set game['mask'][row][col] to True.
    
    If the revealed cell has the bomb, change game state to 'defeat'.

    If the cell has no adjacent bombs, recursively reveal its direct neighbours.
    
    If all the cells except the bomb cells are revealed, change game state to 'victory'.

    Return number of revealed cells in total.

    Parameters:
       game (dict): Game object
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new cells revealed

    >>> game = new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)])
    >>> game['mask'][0][1] = True
    >>> game['revealed'] += 1
    >>> game['covered'] -= 1
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    covered: 3
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    revealed: 5
    state: victory
    total: 8

    >>> game = new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)])
    >>> game['mask'][0][1] = True
    >>> game['revealed'] += 1
    >>> game['covered'] -= 1
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    covered: 6
    dimensions: (2, 4)
    mask:
        [True, True, False, False]
        [False, False, False, False]
    revealed: 2
    state: defeat
    total: 8
    """
    return dig_nd(game, (row, col))


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    rows, cols = game['dimensions']
    board = game['board']
    mask = game['mask']
    result = []
    for i in range(rows):
        result.append([])
        for j in range(cols):
            cell = board[i][j]
            val = (' ' if cell == 0 else str(cell)) if xray or mask[i][j] else '_'
            result[-1].append(val)
    return result


def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    result = render_2d(game, xray)
    result = [''.join(row) for row in result]
    return '\n'.join(result)



# N-D IMPLEMENTATION


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game model dictionary with following properties:
    'dimensions' - sames as input dimensions
    'state' - string, one of following values ('ongoing', 'victory', 'defeat')
    'board' - 2-dimensional array, with cell values of 0-8 (number of neighbour bombs) or '.' (bomb)
    'mask' - 2-dimensional array with boolean cell values, indicating which cells are revealed
    'bombs' - number of bombs
    'covered' -  number of covered cells
    'revealed' - number of revealed cells
    'total' - total number of cells
    
    Parameters:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game object dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    covered: 16
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    revealed: 0
    state: ongoing
    total: 16
    """
    board = new_nd_list(dimensions, 0)
    mask = new_nd_list(dimensions, False)

    def setter(val):
        if val is not None and val != '.':
            return val + 1
        return val
        

    for bomb in bombs:
        set_value(board, bomb, '.')
        for index in get_surrounding_indexes(bomb):
            set_value(board, index, setter)

    total = 1
    for dim in dimensions:
        total *= dim

    return {
        'dimensions': dimensions,
        'board' : board,
        'mask' : mask,
        'state': 'ongoing',
        'revealed': 0,
        'bombs': len(bombs),
        'covered': total,
        'total': total
    }


def dig_nd(game, coordinates):
    """
    Reveal the cell at coordinates and set game['mask'] at coordinates to True.
    
    If the revealed cell has the bomb, change game state to 'defeat'.

    If the cell has no adjacent bombs, recursively reveal its direct neighbours.
    
    If all the cells except the bomb cells are revealed, change game state to 'victory'.

    Return number of revealed cells in total.

    Parameters:
       game (dict): Game object
       coordinates (tuple): Where to start digging

    Returns:
       int: the number of new cells revealed

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> g['mask'][0][1][1] = True
    >>> g['revealed'] += 1
    >>> g['covered'] -= 1
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    covered: 7
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    revealed: 9
    state: ongoing
    total: 16
    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> g['mask'][0][1][1] = True
    >>> g['revealed'] += 1
    >>> g['covered'] -= 1
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    covered: 14
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    revealed: 2
    state: defeat
    total: 16
    """
    if game['state'] in ('defeat', 'victory'):
        return 0

    board = game['board']
    mask = game['mask']

    if get_value(mask, coordinates):
        return 0
    set_value(mask, coordinates, True)

    old_revealed = game['revealed']
    game['revealed'] += 1
    game['covered'] -= 1
    val = get_value(board, coordinates)
    if val == '.':
        game['state'] = 'defeat'
        return 1
    
    if game['covered'] == game['bombs']:
        game['state'] = 'victory'
        return 1

    if val == 0:
        for nindex in get_surrounding_indexes(coordinates):
            shown = get_value(mask, nindex)
            if shown is not None and not shown and get_value(board, nindex) != '.':
                dig_nd(game, nindex)

    return game['revealed'] - old_revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    # doctest.run_docstring_examples(dig_nd, globals(), optionflags=_doctest_flags, verbose=False)
