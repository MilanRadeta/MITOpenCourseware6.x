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
    with open(NAMES_PICKLE, 'rb') as f:
        names = pickle.load(f)
    with open(MOVIES_PICKLE, 'rb') as f:
        movies = pickle.load(f)
    
    id_to_name = {id: name for name, id in names.items()}
    id_to_movie = {id: name for name, id in movies.items()}

    actor_to_actors = {}
    actor_to_movies = {}
    movie_to_actors = {}

    for actor1, actor2, movie in raw_data:
        if actor1 != actor2:
            actor_to_actors.setdefault(actor1, set()).add(actor2)
            actor_to_actors.setdefault(actor2, set()).add(actor1)
            actor_to_movies.setdefault(actor2, set()).add(movie)
            movie_to_actors.setdefault(movie, set()).add(actor2)

        actor_to_movies.setdefault(actor1, set()).add(movie)
        movie_to_actors.setdefault(movie, set()).add(actor1)
        
    return {
        'name_to_id': names,
        'movie_to_id': movies,

        'id_to_name': id_to_name,
        'id_to_movie': id_to_movie,
        
        'actor_to_actors': actor_to_actors,
        'actor_to_movies': actor_to_movies,
        'movie_to_actors': movie_to_actors,
    }


def acted_together(data, actor_id_1, actor_id_2):
    return actor_id_1 == actor_id_2 or actor_id_2 in data['actor_to_actors'][actor_id_1]


def actors_with_bacon_number(data, n):
    ids = { 4724 }
    processed = set()
    while n > 0 and len(ids) > 0:
        n -= 1
        new_ids = {actor_id for id in ids for actor_id in data['actor_to_actors'][id] if actor_id not in processed and actor_id not in ids}
        processed.update(ids)
        ids = new_ids

    return ids


def bacon_path(data, actor_id):
    nodes = [{
        'id': 4724,
        'path': [4724]
    }]
    processed = set()
    i = 0
    while len(nodes) > i:
        node = nodes[i]
        processed.add(node['id'])
        if node['id'] == actor_id:
            return node['path']
        children = data['actor_to_actors'].get(node['id'], [])
        children = [{'id': child, 'path': node['path'] + [child]} for child in children if child not in processed]
        nodes.extend(children)
        i += 1

    return None


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
    with open(LARGE_PICKLE, 'rb') as f:
        large_db = pickle.load(f)
    
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    small_data = transform_data(smalldb)
    large_data = transform_data(large_db)

    names = small_data['name_to_id']
    ids = small_data['id_to_name']
    
    print('Type of data loaded from %s is %s' % (NAMES_PICKLE, type(names)))
    print('Keys are %s' % type(list(names.keys())[0]))
    print('Values are %s' % type(list(names.values())[0]))
    
    name = "Julian O'Donnell"
    print("%s's ID: %s" % (name, names[name]))
    
    id = 1319278
    print("Actor with ID %s: %s" % (id, ids[id]))

    coactors = [
        ('Toi Svane Stepp', 'Cory Pendergast'),
        ('Gerard Depardieu', 'Danny Aiello'),
    ]

    for actor1, actor2 in coactors:
        print('%s acted with %s: %s' % (actor1, actor2, acted_together(small_data, names[actor1], names[actor2])))

    actor_ids = actors_with_bacon_number(large_data, 6)
    actor_names = [large_data['id_to_name'][id] for id in actor_ids]
    print('Actors with Bacon number 6:')
    print(actor_names)

    path = bacon_path(large_data, 1204)
    print('Bacon path to Julia Roberts: %s' % (path,))
