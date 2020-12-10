
graph = {'B': ['C'],
         'C': ['B', 'D'],
         'D': ['C', 'E', 'F'],
         'E': ['D'],
         'F': ['D', 'G', 'H', 'I'],
         'G': ['F'],
         'H': ['F'],
         'I': ['F']}

graph2 = {'F': ['D', 'I', 'G', 'H'],
         'B': ['C'],
         'D': ['C', 'E', 'F'],
         'E': ['D'],
         'H': ['F'],
         'C': ['D', 'B'],
         'G': ['F'],
         'I': ['F']}

gra3 = {'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B']}

grap = {'A': ['B', 'D'],
        'B': ['C', 'A'],
        'C': ['D', 'B'],
        'D': ['A', 'C']}

disgr = {'A': ['B'],
         'B': ['A'],
         'C': ['D'],
         'E': ['D'],
         'F': ['D', 'G', 'H', 'I'],
         'D': ['C', 'E', 'F'],
         'G': ['F'],
         'H': ['F'],
         'I': ['F']}

all_graphs = [gra3, graph, graph2, grap, disgr]