# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) <= 1:
        return [sequence]

    result = []

    first_letter = sequence[0]
    other_letters = sequence[1:]
    perms = get_permutations(other_letters)

    for i in range(len(sequence)):
        for perm in perms:
            new_perm = perm[:i] + first_letter + perm[i:]
            if new_perm not in result:
                result.append(perm[:i] + first_letter + perm[i:])

    return result


if __name__ == '__main__':
    # EXAMPLE

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    inputs = ['abc', 'xyz', 'xxy']
    expected = [
        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'],
        ['xyz', 'xzy', 'yxz', 'zxy', 'yzx', 'zyx'],
        ['xxy', 'xyx', 'yxx'],
    ]

    example_input = 'abc'
    expected = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    perms = get_permutations(example_input)
    for perm in perms:
        if perm not in expected or len(perms) != len(expected):
            print("FAILURE")
            print('Input:', example_input)
            print('Expected Output:', expected)
            print('Actual Output:', perms)
            exit(-1)
    print("SUCCESS")
