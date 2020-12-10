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

    if start not in graph:
        start = list(graph.keys())[0]

    result = True
    for key in graph:
        if key not in coloring:
            result, coloring = colorGraph(graph, key, coloring, colors)
            if not result:
                break
    
    return result, coloring
    


def colorGraph(graph, start=None, coloring=None, colors=None):
    if colors is None:
        colors = [1,2]

    if coloring is None:
        coloring = {}

    if start not in graph:
        start = list(graph.keys())[0]
    
    color = colors[0]
    if start not in coloring:
        coloring[start] = color
    elif coloring[start] != color:
        return False, {}
    else:
        return True, coloring
    
    colors = list(reversed(colors))

    for vertex in graph[start]:
        val, coloring = colorGraph(graph, vertex, coloring, colors)
        if val == False:
            return False, {}
        
    return True, coloring

for g in all_graphs:
    print(g)
    print (bipartiteGraphColor(g))