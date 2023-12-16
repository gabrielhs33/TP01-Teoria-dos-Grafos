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

  def load_image(self, file_name: str) -> Image.Image:
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
      image = Image.open(file_name)
      return image
    except Exception as e:
      # Captura excecoes que podem ocorrer ao abrir a imagem.
      print(f"Error opening image: {e}")

  def get_neighbors(self, x, y, width, height, image: Image.Image) -> list[any]:
    """
    Get non-black neighbors of a pixel in a bitmap image.

    Parameters:
    - x (int): x-coordinate of the pixel.
    - y (int): y-coordinate of the pixel.
    - width (int): Width of the image.
    - height (int): Height of the image.
    - image (Image.Image): The bitmap image.

    Returns:
    - list[any]: A list of coordinates representing non-black neighbors.
    """
    neighbors = []
    # Iterate over neighboring coordinates.
    for i in range(-1, 2):
      for j in range(-1, 2):
        new_x = x + i
        new_y = y + j
        
        # Check if the coordinates are within the image boundaries
        is_within_bounds = 0 <= new_x < width and 0 <= new_y < height

        # Check if the coordinates are not the same as the input pixel
        is_not_same_pixel = (i != 0 or j != 0)

        if is_within_bounds and is_not_same_pixel:
          # Get the color of the pixel in neighboring coordinates.
          pixel_color = image.getpixel((new_x, new_y))
          # Check that the pixel is not black.
          if pixel_color != (0, 0, 0):
            # Adds the coordinates of the non-black pixel to the list of neighbors.
            neighbors.append((new_x, new_y))
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
        
        # Get the color of the current pixel.
        pixel_color = image.getpixel(current_pixel)
        
        # Check if the pixel color is not black.
        if pixel_color != (0, 0, 0):
          # Get non-black neighbors of the current pixel using the get_neighbors function.
          current_neighbors = self.get_neighbors(x, y, width, height, image)
          # Add undirected edges to the graph for each neighbor.
          for pixel in current_neighbors:        
            self.add_undirected_edge(current_pixel, pixel, 1)

  def find_source_and_destination_pixels(self, image_name: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Find the source (red) and destination (green) pixels in the given image.

    Parameters:
    - image (Image.Image): The input image.

    Returns:
    - Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing the coordinates of the source and destination pixels.
    """
    image = self.load_image(image_name)
    width, height = image.size

    source_pixel = None
    destination_pixel = None

    for x in range(width):
      for y in range(height):
        currenct_pixel = (x, y)

        # Get the color of the current pixel.
        pixel_color = image.getpixel(currenct_pixel)

        # Check if the pixel color is red (source).
        if pixel_color == (255, 0, 0):
          source_pixel = (x, y)

        # Check if the pixel color is green (destination):
        if pixel_color == (0, 255, 0):
          destination_pixel = (x, y)
        
        # Break the loop if both source and destination pixel are found. 
        if source_pixel and destination_pixel:
          break
    # Returns the coordinates of the source and destination pixel.
    return (source_pixel, destination_pixel)

  def path_bfs(self, source_pixel: Any, destination_pixel) -> List[Any]:
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
      # Remove the first element of Q.
      u = Q.pop(0)
      for v in self.adj[u]:
        if dist[v] == float("inf"):
          Q.append(v)
          dist[v] = dist[u] + 1
          pred[v] = u        
          # Check if the current pixel is the destination.
          if v == destination_pixel:
            return self.reconstruct_path(pred, source_pixel, destination_pixel)
    # Return an empty list if 'destination_pixel' is not reached.
    return []
  
  def reconstruct_path(self, source_pixel, destination_pixel, pred) -> List[Any]:
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
    path = {destination_pixel}
    currenct_pixel = destination_pixel

    # Traverse the predecessor dictionary to reconstruct the path.
    while currenct_pixel != source_pixel:
      # Move to the predecessor of the currenct pixel.
      currenct_pixel = pred[currenct_pixel]
      # Insert the predecessor at the beginning of the path.
      path.insert(0, currenct_pixel)
    return path
  