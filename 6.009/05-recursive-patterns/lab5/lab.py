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
    Get tuple of indexes surrounding provided index and the provided index itself
    by adding values of index with values of diffs provided by new_nd_diffs.

    Each index is also an n-tuple of ints.

    Parameters:
        index (tuple): n-tuple of ints

    Returns:
        Returns a tuple of 3**n tuples of indexes surrounding the provided index and the provided index itself.

    >>> get_surrounding_indexes((0,))
    ((-1,), (0,), (1,))

    >>> get_surrounding_indexes((3,))
    ((2,), (3,), (4,))

    >>> get_surrounding_indexes((0,0))
    ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))

    >>> get_surrounding_indexes((2,2))
    ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3))
    """
    diffs = new_nd_diffs(len(index))
    result = []
    for pair in zip((index,) * len(diffs), diffs):
        result.append(tuple(map(sum, zip(*pair))))
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

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    dimensions = (num_rows, num_cols)
    board = new_nd_list(dimensions, 0)
    mask = new_nd_list(dimensions, False)

    def setter(val):
        if val is not None and val != '.':
            return val + 1
        return val
        

    for bomb in bombs:
        set_value(board, bomb, '.')
        for index in get_surrounding_indexes(bomb):
            index = tuple(map(sum, zip(*pair)))
            set_value(board, index, setter)

    covered = 1
    for dim in dimensions:
        covered *= dim

    return {
        'dimensions': dimensions,
        'board' : board,
        'mask' : mask,
        'state': 'ongoing',
        'revealed': 0,
        'covered': covered
    }


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    if game['state'] in ('defeat', 'victory'):
        return 0

    index = (row, col)
    board = game['board']
    mask = game['mask']

    if not get_value(mask, index):
        return 0
    set_value(mask, index, True)

    game['revealed'] += 1
    game['covered'] -= 1

    if get_value(board, index) == '.':
        game['state'] = 'defeat'
        return 1
    
    if game['covered'] == 0:
        game['state'] = 'victory'
        return 1


    if game['board'][row][col] == 0:
        num_rows, num_cols = game['dimensions']
        if 0 <= row-1 < num_rows:
            if 0 <= col-1 < num_cols:
                if game['board'][row-1][col-1] != '.':
                    if game['mask'][row-1][col-1] == False:
                        revealed += dig_2d(game, row-1, col-1)
        if 0 <= row < num_rows:
            if 0 <= col-1 < num_cols:
                if game['board'][row][col-1] != '.':
                    if game['mask'][row][col-1] == False:
                        revealed += dig_2d(game, row, col-1)
        if 0 <= row+1 < num_rows:
            if 0 <= col-1 < num_cols:
                if game['board'][row+1][col-1] != '.':
                    if game['mask'][row+1][col-1] == False:
                        revealed += dig_2d(game, row+1, col-1)
        if 0 <= row-1 < num_rows:
            if 0 <= col < num_cols:
                if game['board'][row-1][col] != '.':
                    if game['mask'][row-1][col] == False:
                        revealed += dig_2d(game, row-1, col)
        if 0 <= row < num_rows:
            if 0 <= col < num_cols:
                if game['board'][row][col] != '.':
                    if game['mask'][row][col] == False:
                        revealed += dig_2d(game, row, col)
        if 0 <= row+1 < num_rows:
            if 0 <= col < num_cols:
                if game['board'][row+1][col] != '.':
                    if game['mask'][row+1][col] == False:
                        revealed += dig_2d(game, row+1, col)
        if 0 <= row-1 < num_rows:
            if 0 <= col+1 < num_cols:
                if game['board'][row-1][col+1] != '.':
                    if game['mask'][row-1][col+1] == False:
                        revealed += dig_2d(game, row-1, col+1)
        if 0 <= row < num_rows:
            if 0 <= col+1 < num_cols:
                if game['board'][row][col+1] != '.':
                    if game['mask'][row][col+1] == False:
                        revealed += dig_2d(game, row, col+1)
        if 0 <= row+1 < num_rows:
            if 0 <= col+1 < num_cols:
                if game['board'][row+1][col+1] != '.':
                    if game['mask'][row+1][col+1] == False:
                        revealed += dig_2d(game, row+1, col+1)

    bombs = 0  # set number of bombs to 0
    covered_squares = 0
    for r in range(game['dimensions'][0]):
        # for each r,
        for c in range(game['dimensions'][1]):
            # for each c,
            if game['board'][r][c] == '.':
                if  game['mask'][r][c] == True:
                    # if the game mask is True, and the board is '.', add 1 to
                    # bombs
                    bombs += 1
            elif game['mask'][r][c] == False:
                covered_squares += 1
    bad_squares = bombs + covered_squares
    if bad_squares > 0:
        game['state'] = 'ongoing'
        return revealed
    else:
        game['state'] = 'victory'
        return revealed


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

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    raise NotImplementedError


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    raise NotImplementedError


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
    # doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    doctest.run_docstring_examples(get_surrounding_indexes, globals(), optionflags=_doctest_flags, verbose=False)
