#!/usr/bin/env python3

import pickle
import pathlib

root_folder = pathlib.Path(__file__).parent.absolute().__str__()
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).


def transform_data(raw_data):
    return raw_data


def acted_together(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


def actors_with_bacon_number(data, n):
    raise NotImplementedError("Implement me!")


def bacon_path(data, actor_id):
    raise NotImplementedError("Implement me!")


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


def actor_path(data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(data, film1, film2):
    raise NotImplementedError("Implement me!")


TINY_PICKLE = root_folder + '/resources/tiny.pickle'
SMALL_PICKLE = root_folder + '/resources/small.pickle'
LARGE_PICKLE = root_folder + '/resources/large.pickle'

SMALL_NAMES_PICKLE = root_folder + '/resources/small_names.pickle'
NAMES_PICKLE = root_folder + '/resources/names.pickle'

MOVIES_PICKLE = root_folder + '/resources/movies.pickle'

if __name__ == '__main__':
    with open(SMALL_PICKLE, 'rb') as f:
        smalldb = pickle.load(f)
    
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    with open(NAMES_PICKLE, 'rb') as f:
        names = pickle.load(f)
    
    ids = {names[name]: name for name in names}
    
    print('Type of data loaded from %s is %s' % (NAMES_PICKLE, type(names)))
    print('Keys are %s' % type(list(names.keys())[0]))
    print('Values are %s' % type(list(names.values())[0]))
    
    name = "Julian O'Donnell"
    print("%s's ID: %s" % (name, names[name]))
    
    id = 1319278
    print("Actor with ID %s: %s" % (id, ids[id]))
