import doctest

# NO OTHER IMPORTS!



##################################################
#  Problem 1
##################################################


def screen_savior(image, new_width, new_height):
    def get_pixel_repeated(r, c):
        r = r % image['height']
        c = c % image['width']
        return image['pixels'][r * image['width'] + c]

    return {'width': new_width,
            'height': new_height,
            'pixels': [get_pixel_repeated(r, c)
                       for r in range(new_height)
                       for c in range(new_width)]}


##################################################
#  Problem 2
##################################################


def tourist_graph_search(graph, node):
    all_nodes = {node for connection in graph for node in connection}
    neighbors = {}
    for origin, destination in graph:
        neighbors.setdefault(origin, set()).add(destination)

    agenda = [[node]]
    # here we DON'T want to keep a visited set, since we may need to revisit
    # nodes later (even within the same path!)
    while agenda:
        new = agenda.pop(0)
        set_new = set(new)
        if set_new == all_nodes:
            return new
        for child in neighbors.get(new[-1], []):
            agenda.append(new + [child])
    return None



##################################################
#  Problem 3
##################################################


def count_minesweeper_boards(board):
    # this code contains an unnecessary optimization, in that the is_valid
    # helper function checks to see whether the board _could possibly produce
    # any valid complete boards_ or whether it _already contains a
    # contradiction_.  this allows us to avoid considering many impossible
    # boards.

    # however, we did not expect your solution to do this.  it would be totally
    # valid only to check the validity of a board _if it contained no more
    # blanks_, but otherwise to use a similar structure.

    is_valid = valid_minesweeper_board(board)

    if not is_valid:
        # if we're already at an invalid place, return 0 (this board cannot
        # possibly produce any valid boards)
        return 0

    blanks = [(r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == '_']

    if not blanks:
        return 1

    # this board is incomplete; let's consider marking the first space as a
    # bomb, and not as a bomb, and sum the results
    br, bc = blanks[0]
    out = 0
    for new_val in 'X.':  # let X be not a bomb, but not something we need to check
        new_board = [[(val if (r,c) != (br, bc) else new_val)
                       for c, val in enumerate(row)]
                     for r, row in enumerate(board)]
        out += count_minesweeper_boards(new_board)
    return out


def valid_minesweeper_board(board):
    nrows = len(board)
    ncols = len(board[0])
    for r in range(nrows):
        for c in range(ncols):
            x = board[r][c]
            if x == ' ' or x.isdigit():
                neighbors = [board[nr][nc]
                             for nr in range(r-1, r+2)
                             for nc in range(c-1, c+2)
                             if 0 <= nr < nrows and 0 <= nc < ncols]
                min_bombs = neighbors.count('.')
                max_bombs = min_bombs + neighbors.count('_')
                if not min_bombs <= (int(x) if x != ' ' else 0) <= max_bombs:
                    return False
    return True


if __name__ == "__main__":
    doctest.testmod()
