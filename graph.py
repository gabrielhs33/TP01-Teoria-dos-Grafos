from typing import Any, List, Tuple
from PIL import Image

class Graph:

  def __init__(self):
    self.num_nodes = 0
    self.num_edges = 0
    self.adj = {}

  def add_node(self, node: Any) -> None:
    """
    Adds a node to the graph.

    Parameters:
        node (Any): The node to be added (as a key to a dict)
    """
    try: 
      if self.adj[node] != {}:
        return
    except KeyError:
      self.adj[node] = {}
      self.num_nodes += 1

  def add_nodes(self, nodes: List[Any]) -> None:
    """
    Adds a list of nodes to the graph

    Parameters:
    - nodes (List[Any]): The list of nodes to be added (as keys to a dict)
    """
    for node in nodes:
      self.add_node(node)
      
  def add_directed_edge(self, u, v, weight):
    """
    Add a directed edge from node 'u' to node 'v' with the specified weight.

    Parameters:
    - u: The source node.
    - v: The target node.
    - weight: The weight of the directed edge.

    If the nodes 'u' and 'v' do not exist in the graph, they are added using the 'add_node' function.
    """
    self.add_node(u)
    self.add_node(v)
    self.adj[u][v] = weight
    self.num_edges += 1

  def add_undirected_edge(self, u, v, weight):
    """
    Add a two-way (undirected) edge between nodes 'u' and 'v' with the specified weight.

    Parameters:
    - u: One of the nodes.
    - v: The other node.
    - weight: The weight of the undirected edge.

    This function calls the 'add_edge' function for both (u, v) and (v, u) to represent the undirected edge.
    """
    self.add_directed_edge(u, v, weight)
    self.add_directed_edge(v, u, weight)

  def __repr__(self) -> str:
    str = ""
    for u in self.adj:
      str += f"{u} -> {self.adj[u]}\n"
    return str

  def load_image(self, file: str) -> Image.Image:
    """
    Load an image from a file.

    Parameters:
    - file (str): The image file path.

    Returns:
    - Image.image: An image object representing the loaded image.

    Raises:
    - Exception: If an error occurs when opening the image.
    """
    try:
      # Tenta abrir a imagem usando a biblioteca Pillow (PIL).
      image = Image.open(file)
      return image
    except Exception as e:
      # Captura excecoes que podem ocorrer ao abrir a imagem.
      print(f"Error opening image: {e}")

  def get_neighbors(self, coordinates: tuple, width: int, height: int, image: Image.Image) -> list[tuple[int, int]]:
    """
    Get non-black neighbors of a pixel in a bitmap image.

    Parameters:
    - coordinates (tuple): x and y coordinates of the pixel.
    - width (int): Width of the image.
    - height (int): Height of the image.
    - image (Image.Image): The bitmap image.

    Returns:
    - list[tuple[int, int]]: A list of coordinates representing non-black neighbors.
    """
    neighbors = []
    x, y = coordinates
    
    # Define directions to check for neighbors: left, right, up, down.
    directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    # Iterate over each direction.
    for coordinate_x, coordinate_y in directions:
        if 0 <= coordinate_x < width and 0 <= coordinate_y < height:
          pixel_color = image.getpixel((coordinate_x, coordinate_y))
          if pixel_color != (0, 0, 0):
            neighbors.append((coordinate_x, coordinate_y))
    return neighbors

  def build_graph(self, image_name: str) -> None:
    """
    Build a graph from a bitmap image.

    Parameters:
    - image_name (str): The file path of the bitmap image.

    Returns:
    - None
    """
    # Load the image using the load_image function.
    image = self.load_image(image_name)
    width, height = image.size
        
    # Iterate over all pixels in the image.
    for x in range(width):
      for y in range(height):
        current_pixel = (x, y)
        pixel_color = image.getpixel(current_pixel)
        
        # Check if the pixel is not black.
        if pixel_color in [(255,255,255),(255,0,0),(0,255,0)]:
          
          if pixel_color == (255,0,0):
            source_pixel = current_pixel
          if pixel_color == (0,255,0):
            destination_pixel = current_pixel  
          # Add edges for the non-black pixel.
          self.add_edges_for_pixel(current_pixel, width, height, image)
    return source_pixel,destination_pixel      

  def add_edges_for_pixel(self, coordinates: tuple, width: int, height: int, image: Image.Image) -> None:
    """
    Add edges for a non-black pixel in the graph.

    Parameters:
    - coordinates (tuple): The (x, y) coordinates of the current pixel.
    - width (int): The width of the image.
    - height (int): The height of the image.

    Returns:
    - None
    """
    # Get neighbors of the current pixel.
    current_neighbors = self.get_neighbors(coordinates, width, height, image)

    # Add edges between the current pixel and its neighbors.
    for neighbor_coordinates in current_neighbors:
        self.add_undirected_edge(coordinates, neighbor_coordinates, 1)
        

  def path_bfs(self, source_pixel: any, destination_pixel: any) -> List[Any]:
    """
    Perform Breadth-First Search (BFS) starting from the specified source node.

    Parameters:
    - source_pixel: The source pixel (origin) for the BFS traversal.
    - destination_pixel: The destination pixel to stop the BFS.

    This function explores the graph in breadth-first order
    starting from the given source node 'source_pixel' to the 'destination_pixel' and returns the path.
    """
    dist = {node: float("inf") for node in self.adj}
    pred = {node: None for node in self.adj}
    Q = [source_pixel]
    dist[source_pixel] = 0
    while Q:
      u = Q.pop(0)
      for v in self.adj[u]:
        if dist[v] == float("inf"):
          Q.append(v)
          dist[v] = dist[u] + 1
          pred[v] = u
          if v == destination_pixel:
            return self.reconstruct_path(source_pixel, destination_pixel, pred)
    return []
  
  def reconstruct_path(self, source_pixel: any, destination_pixel: any, pred: dict) -> List[Any]:
    """
    Reconstruct the path from the source pixel to the destination pixel using the predecessor dictionary.

    Parameters:
    - source_pixel: The source pixel of the path.
    - destination_pixel: The destination pixel of the path.
    - pred: The predecessor dictionary obtained from the BFS traversal.

    Returns:
    - List[Any]: The reconstructed path from the source to the destination.
    """
    # Initialize the path with the destination pixel.
    path = [destination_pixel]
    current_pixel = destination_pixel

    # Traverse the predecessor dictionary to reconstruct the path.
    while current_pixel != source_pixel:
      current_pixel = pred[current_pixel]
      path.insert(0, current_pixel)
    return path
  
  def drawn_path(self, path: list, image_name: str) -> None:
    """
    Draw the specified path on the image and save the resulting image.

    Parameters:
    - path: List of coordinates representing the path to be drawn.
    - image_name: The name of the image file to be read and modified.
    """
    image = Image.open(image_name)
    pixels = image.load()
    for v in path:
      x, y = v
      pixels[x, y] = (0, 0, 255)
    # Save the resulting image with the drawn path.
    image.save("./Datasets/nova.bmp")
