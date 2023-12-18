import tkinter
from interface import ImageViewer

# Creating window.
window = tkinter.Tk()

<<<<<<< HEAD
window.title("Image Viewer")
app = ImageViewer(master=window)

app.mainloop()
=======
# Image file name.
image_file = "./Datasets/0_floor.bmp"

# Build the graph from the image.


# Find the source and destination pixels.
source_pixel, destination_pixel = graph.build_graph(image_file)

if source_pixel and destination_pixel:
    print(f"Pixel de origem: {source_pixel}")
    print(f"Pixel de destino: {destination_pixel}")

    # Breadth-first search to find the path from origin to destination.
    path = graph.path_bfs(source_pixel, destination_pixel)

    if path:
        print("Caminho encontrado.")
        graph.drawn_path(path, image_file)
    else:
        print("Nao há caminho possivel.")
else:
    print("Pixel origem e/ou destino nao encontrados.")
       
print(graph.num_nodes)
print(graph.num_edges)
>>>>>>> 561e5166b9b17e43bf4a4653e4c5ec917f23bad7
