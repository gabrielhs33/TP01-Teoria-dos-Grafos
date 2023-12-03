from graph import Graph

g = Graph()
g.build_graph("./Datasets/0_floor.bmp")
print(g.num_nodes)
print(g.num_edges)