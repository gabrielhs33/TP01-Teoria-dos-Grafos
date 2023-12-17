from graph import Graph
from PIL import Image

# Create an instance of the Graph class.
graph = Graph()

# Image file name.
image_file = "./Datasets/0_floor.bmp"

# Build the graph and find the source and destination pixels from the image.
source_pixel, destination_pixel = graph.build_graph(image_file)

if source_pixel and destination_pixel:
    print(f"Pixel de origem: {source_pixel}")
    print(f"Pixel de destino: {destination_pixel}")

    # Breadth-first search to find the path from origin to destination.
    path = graph.path_bfs(source_pixel, destination_pixel)

    if path:
        print("Caminho encontrado.")
        for step in path:
            print(step)
        graph.drawn_path(path, image_file)
    else:
        print("Nao há caminho possivel.")
else:
    print("Pixel origem e/ou destino nao encontrados.")

# print(f"\n{graph}")
print(f"\nNumero de vertices: {graph.num_nodes}")
print(f"Numero de arestas: {graph.num_edges}")
