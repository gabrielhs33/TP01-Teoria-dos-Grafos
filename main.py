from graph import Graph
from PIL import Image

# Create an instance of the Graph class.
graph = Graph()

# Image file name.
image_file = "E:\Pandora's Box\Documents\Faculdade\Teoria dos Grafos\Trabalho Prático 01\Datasets/toy.bmp"

# Build the graph from the image.
graph.build_graph(image_file)

# Find the source and destination pixels.
source_pixel, destination_pixel = graph.find_source_and_destination_pixels(image_file)

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

print(f"\n{graph}")
print(graph.num_nodes)
print(graph.num_edges)
