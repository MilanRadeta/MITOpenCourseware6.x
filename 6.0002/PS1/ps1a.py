###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import pathlib

root_folder = pathlib.Path(__file__).parent.absolute().__str__()

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = {}
    with open(filename, 'r') as cow_file:
        for line in cow_file:
            parts = line.split(',')
            cows[parts[0]] = int(parts[1])
    return cows

# Problem 2


def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    result = []
    weight_to_names = {}
    all_weights = []

    for cow in cows:
        weight = cows[cow]
        if weight not in weight_to_names:
            weight_to_names[weight] = []
            all_weights.append(weight)
        weight_to_names[weight].append(cow)

    all_weights.sort(reverse=True)

    while len(weight_to_names) > 0:
        trip = []
        new_weights = all_weights.copy()
        current_limit = limit

        for weight in all_weights:
            while (weight in weight_to_names):
                if current_limit >= weight:
                    current_limit -= weight
                    cow = weight_to_names[weight].pop()
                    trip.append(cow)
                    if len(weight_to_names[weight]) <= 0:
                        new_weights.remove(weight)
                        del weight_to_names[weight]
                else:
                    break
            if current_limit == 0:
                break

        all_weights = new_weights
        result.append(trip)

    return result

# Problem 3


def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    parts = get_partitions(cows.keys())
    min_trips = len(cows) + 1
    best_trips = None
    for trips in parts:
        if len(trips) < min_trips:
            weights_per_trips = [[cows[cow] for cow in trip] for trip in trips]
            weight_fits = [
                sum(weights) <= limit for weights in weights_per_trips]
            if all(weight_fits):
                min_trips = len(trips)
                best_trips = trips
    return best_trips


# Problem 4


def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    file = 'ps1_cow_data.txt'
    cows = load_cows(root_folder + '/' + file)

    start = time.time()
    trips = greedy_cow_transport(cows)
    end = time.time()
    print('GREEDY COW TRANSPORT')
    print("Trips count: ", len(trips))
    print("Calculated in: ", end - start, 's')
    print()

    start = time.time()
    trips = brute_force_cow_transport(cows)
    end = time.time()
    print('BRUTE FORCE COW TRANSPORT')
    print("Trips count: ", len(trips))
    print("Calculated in: ", end - start, 's')
    print()


files = ['ps1_cow_data.txt', 'ps1_cow_data_2.txt']
for file in files:
    cows = load_cows(root_folder + '/' + file)

    trips = greedy_cow_transport(cows)
    print("Greedy cow transport: ", trips)

    trips = brute_force_cow_transport(cows)
    print("Brute force cow transport: ", trips)
    print()

compare_cow_transport_algorithms()
