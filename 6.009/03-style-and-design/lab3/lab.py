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
    actor_to_actors = data['actor_to_actors']
    return actor_id_1 == actor_id_2 or actor_id_2 in actor_to_actors[actor_id_1]


def actors_with_bacon_number(data, n):
    actor_to_actors = data['actor_to_actors']
    ids = { 4724 }
    processed = set()
    while n > 0 and len(ids) > 0:
        n -= 1
        new_ids = {actor_id for id in ids for actor_id in actor_to_actors[id] if actor_id not in processed and actor_id not in ids}
        processed.update(ids)
        ids = new_ids

    return ids


def bacon_path(data, actor_id):
    return actor_to_actor_path(data, 4724, actor_id)


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    return actor_path(data, actor_id_1, lambda id: id == actor_id_2)


def movies_for_actor_path(data, path):
    actor_to_movies = data['actor_to_movies']
    prev = None
    result = []
    for id in path:
        if prev is None:
            prev = id
            continue
        movies = actor_to_movies[prev].intersection(actor_to_movies[id]),
        movie = next(iter(movies[0]))
        result.append(movie)
        prev = id
    return result

def actor_path(data, actor_id_1, goal_test_function):
    actor_to_actors = data['actor_to_actors']
    nodes = [{
        'id': actor_id_1,
        'path': [actor_id_1]
    }]
    processed = set()
    i = 0
    while len(nodes) > i:
        node = nodes[i]
        processed.add(node['id'])
        if goal_test_function(node['id']):
            return node['path']
        children = actor_to_actors.get(node['id'], [])
        children = [{
            'id': child,
            'path': node['path'] + [child]
        } for child in children if child not in processed]
        nodes.extend(children)
        i += 1

    return None


def actors_connecting_films(data, film1, film2):
    raise NotImplementedError("Implement me!")

def convert(data, val, key):
    if type(val) in (list, tuple, set):
        return type(val)(data[key][v] for v in val)
    return data[key][val]

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
    actor_names = convert(large_data, actor_ids, 'id_to_name')
    print('Actors with Bacon number 6:')
    print(actor_names)

    path = bacon_path(large_data, 1204)
    print('Bacon path to Julia Roberts: %s' % (path))

    name = 'Katherine Griffith'
    id = convert(large_data, name, 'name_to_id')
    path = bacon_path(large_data, id)
    path = convert(large_data, path, 'id_to_name')
    print('Bacon path to %s: %s' % (name, path))

    names = ('Gregory Michaels', 'Michael Yarmush')
    ids = convert(large_data, names, 'name_to_id')
    path = actor_to_actor_path(large_data, ids[0], ids[1])
    path = convert(large_data, path, 'id_to_name')
    print('Path from %s to %s: %s' % (names[0], names[1], path))

    names = ('Kevin Bacon', 'Julia Roberts')
    ids = convert(large_data, names, 'name_to_id')
    path = actor_to_actor_path(large_data, ids[0], ids[1])
    path = movies_for_actor_path(large_data, path)
    print('Movie path from %s to %s: %s' % (names[0], names[1], path))

    names = ('Kathleen Quinlan', 'Iva Ilakovac')
    ids = convert(large_data, names, 'name_to_id')
    path = actor_to_actor_path(large_data, ids[0], ids[1])
    path = movies_for_actor_path(large_data, path)
    path = convert(large_data, path, 'id_to_movie')
    print('Movie path from %s to %s: %s' % (names[0], names[1], path))
