#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url
import pathlib

root_folder = pathlib.Path(__file__).parent.absolute().__str__()

# NO ADDITIONAL IMPORTS!


ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}


def build_auxiliary_structures(nodes_filename, ways_filename):
    """
    Create any auxiliary structures you are interested in, by reading the data
    from the given filenames (using read_osm_data)
    """
    return None


def find_short_path_nodes(aux_structures, node1, node2):
    """
    Return the shortest path between the two nodes

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        node1: node representing the start location
        node2: node representing the end location

    Returns:
        a list of node IDs representing the shortest path (in terms of
        distance) from node1 to node2
    """
    raise NotImplementedError


def find_short_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """
    raise NotImplementedError


def find_fast_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    raise NotImplementedError


PICKLE_NODES = root_folder + '/resources/cambridge.nodes'
PICKLE_WAYS = root_folder + '/resources/cambridge.ways'

if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    nodes_count = 0
    name_count = 0
    id = None
    name = '77 Massachusetts Ave'
    for node in read_osm_data(PICKLE_NODES):
        nodes_count += 1
        node_name = node['tags'].get('name', None)
        if node_name is not None:
            name_count += 1
            if node_name == name:
                id = node['id']
    print('%s nodes' % nodes_count)
    print('%s names nodes' % name_count)
    print('%s - %s' % (id, name))
    
    ways_count = 0
    one_way_count = 0
    for way in read_osm_data(PICKLE_WAYS):
        ways_count += 1
        one_way = way['tags'].get('oneway', False)
        if one_way == 'yes':
            one_way_count += 1
    
    print('%s ways' % ways_count)
    print('%s one-way streets' % one_way_count)
