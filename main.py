from graph import Graph

g = Graph()
origin , destiny = g.build_graph("./Datasets/toy.bmp")

print(g.num_nodes)
print(g.num_edges)
c = g.recover_path(origin,destiny,g.bfs(origin))
print(c)
g.drawn_map(c,"./Datasets/toy.bmp")