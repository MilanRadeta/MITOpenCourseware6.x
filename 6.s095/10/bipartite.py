#Programming for the Puzzled -- Srini Devadas
#A Weekend to Remember
#This puzzle deals with the problem of inviting friends to dinner over two days
#such that no two of your friends who dislike each other are invited on the same
#day.  This can be done if the graph is a bipartite graph.

#The code determines if a graph is bipartite or not. If the graph can be colored
#using two colors, it is bipartite, else it is not.

from graphs import all_graphs

def bipartiteGraphColor(graph, start=None, coloring=None, colors=None):
    if colors is None:
        colors = [1,2]

    if coloring is None:
        coloring = {}

    if start is None:
        start = list(graph.keys())[0]

    previous = None
    result = True
    for key in graph:
        if key not in coloring:
            result, coloring, previous = colorGraph(graph, key, coloring, colors)
            if not result:
                break
    
    return result, coloring, previous
    


def colorGraph(graph, start=None, coloring=None, colors=None, previous=None):
    if previous is None:
        previous = []

    if colors is None:
        colors = [1,2]

    if coloring is None:
        coloring = {}

    if start is None:
        start = list(graph.keys())[0]
    
    previous.append(start)
    color = colors[0]

    if start not in coloring:
        coloring[start] = color
    elif coloring[start] != color:
        return False, {}, previous
    else:
        return True, coloring, None
    
    colors = list(reversed(colors))

    for vertex in graph[start]:
        val, coloring, last_prev = colorGraph(graph, vertex, coloring, colors, previous.copy())
        if val == False:
            return False, {}, last_prev
        
    return True, coloring, None

def findPath(graph, start=None, end=None, path=None):
    if path is None:
        path = []

    if start is None:
        start = list(graph.keys())[0]

    if end is None:
        end = list(graph.keys())[0]
    
    path.append(start)

    if start == end:
        return path

    for vertex in graph[start]:
        if vertex not in path:
            val = findPath(graph, vertex, end, path.copy())
            if val is not None:
                return val
        
    return None

for g in all_graphs:
    print('Graph:', g)
    val, coloring, cyclic = bipartiteGraphColor(g)
    if cyclic is not None:
        print('Here is a cyclic path that cannot be colored', cyclic)
    print('Bipartite:', (val, coloring))
    print('Path from B to I:', findPath(g, 'B', 'I'))
    print()