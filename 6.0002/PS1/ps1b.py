###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================

# Problem 1
from time import time


def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    if isinstance(egg_weights, tuple):
        egg_weights = list(egg_weights)

    memokey = len(egg_weights)
    if target_weight <= 0 or memokey == 0:
        return 0

    if memokey not in memo:
        memo[memokey] = max(egg_weights)

    weight = memo[memokey]

    if target_weight >= weight:
        return 1 + dp_make_weight(egg_weights, target_weight - weight, memo)

    filtered_eggs = [w for w in egg_weights[:-1] if w <= target_weight]

    return dp_make_weight(filtered_eggs, target_weight, memo)


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    # print("Egg weights = ", egg_weights)
    print("n = ", n)
    start = time()
    # print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    end = time()
    print("Time:", end - start, 's')
    print()
