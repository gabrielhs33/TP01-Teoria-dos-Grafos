from PIL import Image

class Graph:

    def __init__(self) -> None:

        self.num_nodes = 0
        self.num_edges = 0
        self.adj = {}

    def  add_node (self, node: any) -> None:

        try:
            if self.adj[node] != {}:
                return
        except KeyError:
            self.adj[node] = {}
            self.num_nodes += 1

    def add_nodes(self, nodes: list[any]) -> None:
        
        for node in nodes:
            self.add_node(node)

    def add_directed_edge(self, u, v, weight):

        self.add_node(u)
        self.add_node(v)
        self.adj[u][v] = weight
        self.num_edges += 1

    def add_undirected_edge(self, u, v, weight):
        
        self.add_directed_edge(u, v, weight)
        self.add_directed_edge(v, u, weight)

    #return a list of neighborns of a pixel
    def get_neighbors(self, x, y, width, height, image:Image.Image) -> list[any]:
   
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x, new_y = x + i, y + j
                if 0 <= new_x < width and 0 <= new_y < height and (i != 0 or j != 0):
                    pixel_color = image.getpixel((new_x, new_y))
                    if pixel_color != (0,0,0):
                        neighbors.append((new_x, new_y))
        return neighbors

    def load_image(self, file_name:str) -> Image.Image:

        try:
            
            image = Image.open(file_name)
            
        except KeyError:
            print('error to load image')

        return image
    
    def build_graph(self, image_name:str) -> None:

        image = self.load_image(image_name)
        
        width, height = image.size
        print(width)
        print(height)

        for x in range (width):
            for y in range (height):
                current_pixel = (x, y)
                pixel_color = image.getpixel(current_pixel)
                if pixel_color != (0,0,0):
                    current_neighbors = self.get_neighbors(x, y, width, height,image)
                    for pixel in current_neighbors:        
                        self.add_undirected_edge(current_pixel, pixel, 1)

    

        

