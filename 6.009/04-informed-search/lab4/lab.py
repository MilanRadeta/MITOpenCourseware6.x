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
    all_nodes = {}
    for node in read_osm_data(nodes_filename):
        id = node['id']
        node['loc'] = (node['lat'], node['lon'])
        all_nodes[id] = node


    nodes = {}
    ways = {}
    digraph = {}
    distances = {}
    speeds = {}
    locations = {}
    for way in read_osm_data(ways_filename):
        id = way['id']
        highway = way['tags'].get('highway', None)
        if highway in ALLOWED_HIGHWAY_TYPES:
            ways[id] = way
            path = way['nodes']
            is_one_way = way['tags'].get('oneway', 'no') == 'yes'
            speed = way['tags'].get('maxspeed_mph', DEFAULT_SPEED_LIMIT_MPH[highway])
            for i in range(len(path) - 1):
                ids = (path[i], path[i+1])
                for id in ids:
                    nodes[id] = all_nodes[id]
                    locations[id] = nodes[id]['loc']
                    if speed > speeds.get(id, 0):
                        speeds[id] = speed
                distance = distance_between_node_ids(nodes, ids[0], ids[1])

                distances[ids] = distance
                digraph.setdefault(ids[0], set()).add(ids[1])
                if not is_one_way:
                    ids = (ids[1], ids[0])
                    distances[ids] = distance
                    digraph.setdefault(ids[0], set()).add(ids[1])
    
    return {
        'nodes': nodes,
        'ways': ways,
        'digraph': digraph,
        'distances': distances,
        'speeds': speeds,
        'locations': locations
    }


def find_short_path_nodes(aux_structures, node1, node2, cost_fun=None, heuristic=None, verbose=False):
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
    if heuristic is None:
        heuristic = lambda item, goal: 0
    if cost_fun is None:
        cost_fun = lambda prev_item, item: distances[(prev_item, item)]
    digraph = aux_structures['digraph']
    distances = aux_structures['distances']
    agenda = [(node1, (node1,), 0)]
    expanded = set()
    total_count = 0
    while len(agenda) > 0:
        node, path, cost = agenda.pop()
        total_count += 1
        if node in expanded:
            continue
        
        if node == node2:
            if verbose:
                print('Processed paths: %s' % len(expanded))
                print('Total pull-offs: %s' % total_count)
            return path
        expanded.add(node)
        children = digraph.get(node, set())
        children = {
            (child, path + (child,), cost + cost_fun(node, child) + heuristic(child, node2))
            for child in children
            if child not in expanded
        }
        agenda.extend(children)
        agenda.sort(key=lambda item: item[2], reverse=True)

    return None


def get_closest_node(aux_structures, loc):
    locs = aux_structures['locations']
    best = None
    min_cost = None
    for id, nloc in locs.items():
        cost = great_circle_distance(nloc, loc)
        if best is None or cost < min_cost:
            best = id
            min_cost = cost
    return best

def get_closest_nodes(aux_structures, locs):
    found = []
    for loc in locs:
        best = get_closest_node(aux_structures, loc)
        found.append(best)
    return found


def find_short_path(aux_structures, loc1, loc2, cost_fun=None, heuristic=None, verbose=False):
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
    found = get_closest_nodes((loc1, loc2))
    result = find_short_path_nodes(aux_structures, found[0], found[1], cost_fun=cost_fun, heuristic=heuristic, verbose=verbose)
    if result is None:
        return result

    locs = aux_structures['locations']
    result = tuple(locs[id] for id in result)

    return result


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
    found = get_closest_nodes(aux_structures, (loc1, loc2))
    locs = aux_structures['locations']
    speeds = aux_structures['speeds']
    distances = aux_structures['distances']
    cost_fun = lambda prev_item, item: distances[(prev_item, item)] / speeds[item]
    # cost_fun = lambda prev_item, item: distances[(prev_item, item)] / ((speeds[item] + speeds[prev_item]) / 2)
    # heuristic = lambda item, goal: speeds[item]
    heuristic = lambda item, goal: great_circle_distance(locs[item], locs[goal]) / speeds[item]
    # heuristic = None
    result = find_short_path_nodes(aux_structures, found[0], found[1], cost_fun=cost_fun, heuristic=heuristic)
    if result is None:
        return result

    locs = aux_structures['locations']
    result = tuple(locs[id] for id in result)

    return result

def distance_between_nodes(node1, node2):
    loc1 = (node1['lat'], node1['lon'])
    loc2 = (node2['lat'], node2['lon'])
    return great_circle_distance(loc1, loc2)

def distance_between_node_ids(nodes, node1, node2):
    node1 = nodes[node1]
    node2 = nodes[node2]
    return distance_between_nodes(node1, node2)


CAMBRIDGE_NODES = root_folder + '/resources/cambridge.nodes'
CAMBRIDGE_WAYS = root_folder + '/resources/cambridge.ways'

MIDWEST_NODES = root_folder + '/resources/midwest.nodes'
MIDWEST_WAYS = root_folder + '/resources/midwest.ways'

MIT_NODES = root_folder + '/resources/mit.nodes'
MIT_WAYS = root_folder + '/resources/mit.ways'

if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    nodes_count = 0
    name_count = 0
    id = None
    name = '77 Massachusetts Ave'
    for node in read_osm_data(CAMBRIDGE_NODES):
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
    for way in read_osm_data(CAMBRIDGE_WAYS):
        ways_count += 1
        one_way = way['tags'].get('oneway', 'no')
        if one_way == 'yes':
            one_way_count += 1
    
    print('%s ways' % ways_count)
    print('%s one-way streets' % one_way_count)

    loc1 = (42.363745, -71.100999)
    loc2 = (42.361283, -71.239677)
    dist = great_circle_distance(loc1, loc2)
    print('Distance between %s and %s: %s miles' % (loc1, loc2, dist))
    
    nodes = {
        233941454: None,
        233947199: None
    }
    count = 0
    for node in read_osm_data(MIDWEST_NODES):
        id = node['id']
        if id in nodes:
            count += 1
            nodes[id] = node
            if count == 2:
                break
    ids = tuple(nodes.keys())
    dist = distance_between_node_ids(nodes, ids[0], ids[1])
    print('Distance between %s and %s: %s miles' % (ids[0], ids[1], dist))

    id = 21705939
    way = None
    for way in read_osm_data(MIDWEST_WAYS):
        if way['id'] == id:
            break

    nodes = {}
    path = way['nodes']
    for node in read_osm_data(MIDWEST_NODES):
        id = node['id']
        if id in path:
            nodes[id] = node
            if len(nodes) == len(path):
                break

    dist = 0
    for i in range(len(path) - 1):
        dist += distance_between_node_ids(nodes, path[i], path[i+1])
    print('Total length of way with id %s: %s miles' % (way['id'], dist))

    midwest_structure = build_auxiliary_structures(MIDWEST_NODES, MIDWEST_WAYS)
    loc = (41.4452463, -89.3161394)
    best = get_closest_node(midwest_structure, loc)
    print('Nearest relevant node to the location %s has id %s' % (loc, best))

    cambridge_structure = build_auxiliary_structures(CAMBRIDGE_NODES, CAMBRIDGE_WAYS)
    locs = cambridge_structure['locations']
    loc1 = (42.3858, -71.0783)
    loc2 = (42.5465, -71.1787)
    path1 = find_short_path(cambridge_structure, loc1, loc2, verbose=True)
    path2 = find_short_path(cambridge_structure, loc1, loc2, verbose=True, heuristic=lambda item, goal: great_circle_distance(locs[item], locs[goal]))
    print('Path lengths: %s vs %s' % (len(path1), len(path2)))


