import os
import doctest

import sys
sys.setrecursionlimit(3000)

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################

class InterpolatedList(list):
    def __getitem__(self, x):
        if not 0 <= x <= len(self)-1:
            raise IndexError
        if isinstance(x, int):
            return list.__getitem__(self, x)
        else:
            lowix = int(x) if x >= 0 else (int(x)-1)
            low = list.__getitem__(self, lowix)
            high = list.__getitem__(self, lowix + 1)

            dist = x - lowix
            return low + (high-low) * dist

    def __setitem__(self, ix, elt):
        if not (isinstance(elt, (int, float)) and isinstance(ix, int)):
            raise TypeError
        list.__setitem__(self, ix, elt)


##################################################
#  Problem 2
##################################################

def biggest_island(world):
    height = world['height']
    width = world['width']
    markers = world['markers']

    # helper to find the neighbors of a given spot
    def neighbors(r, c):
        return {(nr, nc) for (nr, nc) in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
                if 0 <= nr < height and 0 <= nc < width}

    # not necessary, but some of the code below is easier if we have the
    # mapping specified in another way (char -> locations, rather than location
    # -> char)
    char_to_loc = {char: set() for char in set(char_to_loc.values())}
    for loc, char in markers.items():
        char_to_loc[char].add(loc)

    for char, locs in char_to_loc.items():
        biggest = 0
        while True:
            island = set()
            current_layer = {locs.pop()}
            while current_layer:
                island |= current_layer
                next_layer = set()
                for loc in current_layer:
                    next_layer |= (neighbors(*loc) & locs)
                    locs -= valid_neighbors
                current_layer = next_layer
            new_size = len(island)
            biggest = max(biggest, new_size)

    return biggest


##################################################
#  Problem 3
##################################################


def distribute_inventory(wishlist, inventory):
    if not wishlist:
        return {}

    for person in wishlist:
        new_wishlist = {k: v for k,v in wishlist.items() if k != person}
        for ix, toy in enumerate(wishlist[person]):
            if inventory.get(toy, 0) > 0:
                new_inventory = {k: (v-1 if k == toy else v)
                                 for k,v in inventory.items()}
                subresult = distribute_toys(new_wishlist, new_inventory)
                if subresult is not None:
                    subresult[person] = toy
                    return subresult
        return None



if __name__ == '__main__':
    doctest.testmod()

