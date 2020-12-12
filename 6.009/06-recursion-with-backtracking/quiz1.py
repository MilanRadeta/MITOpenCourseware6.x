import doctest

# NO OTHER IMPORTS!



##################################################
#  Problem 1
##################################################


def wordsearch(board, word):
    for r, row in enumerate(board):
        for c in range(len(row)):
            right_word = ''.join(row[c:c+len(word)])
            down_word = ''.join(board[i][c] for i in range(r, min(r+len(word), len(board))))

            if word == right_word or word == down_word:
                return (r, c)
    return None


##################################################
#  Problem 2
##################################################


def print_family_tree(tree, indent=0):
    """Feel free to call this handy function to print trees in more-readable style."""
    print(' ' * indent, tree[0])
    for parent in tree[1:]:
        print_family_tree(parent, indent+2)


def approximated_family_trees(tree):
    assert len(tree) in [1, 3]

    if len(tree) == 1:
        return [tree]
    else:
        return [[tree[0]]] + [[tree[0], tr1, tr2]
                              for tr1 in approximated_family_trees(tree[1])
                              for tr2 in approximated_family_trees(tree[2])]


##################################################
#  Problem 3
##################################################


def immutable_board(board):
    return tuple(tuple(row) for row in board)


def free_food_bonanza(board):
    # here, we represent state as a tuple of location, followed by a frozenset
    # of all food locations.  this is definitely not necessary (you could, for
    # example, use immutable_board to store the whole board as your state,
    # which would work as well).  but it is important that your state contain
    # information not only about the student's current position, but also about
    # the positions of the remaining foods).  doing so allows us to use our
    # regular BFS to solve this problem, without any additional logic for
    # handling multiple targets.
    start_state = (find_character(board, 'S')[0], frozenset(find_character(board, 'F')))

    possible_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def successors(state):
        (r, c), foods = state
        for dr, dc in possible_moves:
            nr, nc = r + dr, c + dc
            # only consider moves that leave us in bounds and are not a wall
            if 0<=nr<len(board) and 0<=nc<len(board[nr]) and board[nr][nc] != 'W':
                # if this location has a food, remove it
                yield (nr, nc), (foods - {(nr, nc)} if board[nr][nc] == 'F' else foods)

    def goal(state):
        return state[1] == frozenset()

    # in the agenda, we can store the terminal vertex and the length of the
    # path (no need to store the actual path we find)
    agenda = [(start_state, 0)]
    visited = {start_state}
    while agenda:
        state, length = agenda.pop(0)
        if goal(state):
            return length
        for child in successors(state):
            if child not in visited:
                visited.add(child)
                agenda.append((child, length + 1))
    return None


def find_character(board, character):
    return [(r, c)
            for r, row in enumerate(board)
            for c in range(len(row))
            if row[c] == character]


if __name__ == "__main__":
    doctest.testmod()
