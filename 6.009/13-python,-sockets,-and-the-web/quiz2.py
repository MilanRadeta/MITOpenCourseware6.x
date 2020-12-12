import os
import doctest

# NO OTHER IMPORTS!



##################################################
#  Problem 1
##################################################

def find_paths(grid):
    num_rows = len(grid)
    num_cols = len(grid[0])

    def neighbors(loc):
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = loc[0] + dr, loc[1] + dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols:
                yield (nr, nc)

    def find_character(char):
        return [(row, col) for row in range(num_rows)
                           for col in range(num_cols)
                if grid[row][col] == char]

    start = find_character('S')[0]
    goal = find_character('G')[0]
    agenda = [(start, )]
    while agenda:
        current = agenda.pop(0)

        for neighbor in neighbors(current[-1]):
            # changed: replace visited set with a check about no repeated
            # states within the same path (the visited set prevents us from
            # considering multiple paths to the same location, which is
            # necessary)
            if grid[neighbor[0]][neighbor[1]] == 'X' or neighbor in current:
                continue
            new_path = current + (neighbor, )
            if neighbor == goal:
                # changed: instead of returning the first path we found, yield
                # it and continue on
                yield new_path
            agenda.append(new_path)


##################################################
#  Problem 2
##################################################

knot_lengths = {
    'bowline knot': 10,
    'stopper knot': 5,
    'clove hitch': 7.1,
    'sheet bend': 2.9,
    'rolling hitch': 3.8,
    'half hitch': 1,
    'square knot': 9,
    'cleat hitch': 6.4,
    'figure-8 knot': 7,
    'boom hitch': 2.5,
    'davy knot': 9,
    "farmer's loop knot": 7,
    'orvis knot': 3,
    'palomar knot': 7,
    'slip knot': 9,
    'snell knot': 1.2,
    'trilene knot': 4.8,
    'timber hitch': 3
}


def rope_count(knots, seller_length):

    def helper(knots, current_lengths):
        if len(knots) == 0:
            return len(current_lengths)

        one_knot, rest = knots[0], knots[1:]
        smallest = None # best result so far
        knot_length = knot_lengths[one_knot]

        # try using each left-over piece we currently have
        for jx, length in enumerate(current_lengths):
            if knot_lengths[one_knot] <= length:
                # we could use this segment
                new_val = length - knot_length
                new_lengths = [(i if ix != jx else new_val)
                               for ix, i in enumerate(current_lengths)]
                result = helper(rest, new_lengths)
                if smallest is None or result < smallest:
                    smallest = result

        # try buying a new rope
        result = helper(rest, current_lengths + [seller_length - knot_length])
        if smallest is None or result < smallest:
            smallest = result

        return smallest

    return helper(knots, [])


##################################################
#  Problem 3
##################################################

class Pond:
    def __init__(self):
        self.timestep = 0
        self.free_fish = {}
        self.caught_fish = []

    def add_fish(self, location, fish):
        self.free_fish.setdefault(location, []).append(fish)

    def catch_fish(self, location, bait):

        candidate_fish = []
        for fsh in self.free_fish.get(location, []):
            if bait in fsh.eats and (fsh.arrive_at <= self.timestep < fsh.arrive_at + fsh.duration):
                candidate_fish.append((fsh.weight, fsh))

        self.timestep += 1

        if not candidate_fish:
            return None

        candidate_fish.sort()
        _, best_fish = candidate_fish[0]
        self.free_fish[location].remove(best_fish)
        self.caught_fish.append(best_fish)
        return best_fish

    def wait(self, n):
        self.timestep += n

    def weight_caught(self):
        return sum(fish.weight for fish in self.caught_fish)




if __name__ == "__main__":
    doctest.testmod()
