from PIL import Image

def load_image(file: str) -> Image.Image:
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
      # Try to open the image using the Pillow library (PIL).
      image = Image.open(file)
      return image
    except Exception as e:
      print(f"Error opening image: {e}")
