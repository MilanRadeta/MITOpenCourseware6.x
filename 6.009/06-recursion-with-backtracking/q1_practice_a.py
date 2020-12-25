def trailing_weighted_average(S, W):
    return [sum(W[j] * S[max(i-j, 0)] for j in range(len(W))) for i in range(len(S))]

assert trailing_weighted_average([1, 2], [0.8, 0.7]) == [1.5, 2.3]
assert trailing_weighted_average([1, 5, 6, 7], [1]) == [1, 5, 6, 7]
assert trailing_weighted_average([1, 5, 6, 7], [0.5, 0.5]) == [1.0, 3.0, 5.5, 6.5]
assert trailing_weighted_average([1, 5, 6, 7], [0, 1]) == [1, 1, 5, 6]
assert trailing_weighted_average([1, 5, 6, 7], [1, 0]) == [1, 5, 6, 7]
assert trailing_weighted_average([1, 5, 6, 7], [2, 0, 0, 0, 100]) == [102, 110, 112, 114]

def all_consecutives(vals, n):
    if n == 0 or n > len(vals):
        return set()

    if n == 1:
        return {(val,) for val in vals}
    
    if n == 2:
        return {(val, other) for val in vals for other in vals if other - val == 1}

    return {
        (val,) + s for val in vals
        for s in all_consecutives({other for other in vals if other > val}, n - 1)}

    
assert all_consecutives({0, 1, 2, 3, 4}, 1) == {(0,), (1,), (2,), (3,), (4,)}
assert all_consecutives({0, 1, 2, 3, 4}, 2) == {(0, 1), (3, 4), (2, 3), (1, 2)}
assert all_consecutives({0, 1, 2, 3, 4}, 5) == {(0, 1, 2, 3, 4)}
assert all_consecutives({0, 1, 2, 3, 4}, 6) == set()
assert all_consecutives({0, 2, 4}, 1) == {(2,), (0,), (4,)}
assert all_consecutives({0, 2, 4}, 2) == set()
assert all_consecutives({0, 83, 2, 3, 81, 7, 82}, 2) == {(81, 82), (2, 3), (82, 83)}

def cost_to_consume(seq1, seq2):
    agenda = [(seq1, seq2, 0)]
    min_cost = None
    while len(agenda) > 0:
        seq1, seq2, cost = agenda.pop()
        if min_cost is not None and cost > min_cost:
            continue
        if len(seq1 + seq2) == 0:
            if min_cost is None or min_cost > cost:
                min_cost = cost
            continue
        if len(seq1) > 0 and len(seq2) > 0:
            if seq1[0] == seq2[0]:
                agenda.append((seq1[1:], seq2[1:], cost))
            else:
                agenda.append((seq1[1:], seq2[1:], cost + 1))
        if seq1:
            agenda.append((seq1[1:], seq2, cost + 1))
        if seq2:
            agenda.append((seq1, seq2[1:], cost + 1))
    return min_cost

    
assert cost_to_consume('ab', 'b') == 1
assert cost_to_consume('mast', 'mast') == 0
assert cost_to_consume('mast', 'must') == 1
assert cost_to_consume('misty', 'must') == 2
assert cost_to_consume('color', 'colour') == 1
assert cost_to_consume('car', 'boat') == 3
assert cost_to_consume('frog', 'apple') == 5
assert cost_to_consume('aba', 'bbb') == 2
assert cost_to_consume('aba', 'bab') == 2
