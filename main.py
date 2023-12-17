from graph import Graph
from PIL import Image

<<<<<<< HEAD
# Cria uma instancia da classe Graph.
graph = Graph()

# Nome do arquivo de imagem.
image_file = "E:\Pandora's Box\Documents\Faculdade\Teoria dos Grafos\Trabalho Prático 01\Datasets/toy_v2.bmp"

# Construir o grafo a partir da imagem
graph.build_graph(image_file)

# Encontrar os pixels de origem (vermelho) e destino (verde).
source_pixel, destination_pixel = graph.find_source_and_destination_pixels(image_file)

if source_pixel and destination_pixel:
    print(f"Pixel de origem: {source_pixel}")
    print(f"Pixel de destino: {destination_pixel}")

    # Busca em largura para encontrar o caminho da origem ate destino.
    path = graph.path_bfs(source_pixel, destination_pixel)

    if path:
        print("Caminho encontrado.")
        for step in path:
            print(step)
        graph.drawn_map(path, image_file)
    else:
        print("Nao há caminho possivel.")
else:
    print("Pixel origem e/ou destino nao encontrados.")

print()
print(graph.num_nodes)
print(graph.num_edges)
=======
g = Graph()
origin , destiny = g.build_graph("./Datasets/toy.bmp")

print(g.num_nodes)
print(g.num_edges)
c = g.recover_path(origin,destiny,g.bfs(origin))
print(c)
g.drawn_map(c,"./Datasets/toy.bmp")
>>>>>>> 1f51be830e56b5e4b0739a46d05a1e45a94ccf61
