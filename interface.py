import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from drawn_path import drawn_path
from graph import Graph

class ImageViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.graph = Graph()
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold buttons.
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, pady=10) 

        # Button to upload an image.
        self.upload_button = tk.Button(button_frame, text="Carregar Imagem", command=self.upload_image)
        self.upload_button.pack(side=tk.LEFT, padx=10)
        
        # Button to show the path on the image.
        self.show_path_button = tk.Button(button_frame, text="Exibir Caminho", command=self.show_path, state=tk.DISABLED)
        self.show_path_button.pack(side=tk.LEFT, padx=10)

        # Canvas to show image.
        self.canvas = tk.Canvas(self, bg="white", width=800, height=600)
        self.canvas.pack(side=tk.LEFT)  

        # Zoom and move variables
        self.bind_all("<KeyPress>", self.on_key_press)
        self.bind_all("<KeyRelease>", self.on_key_release)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_stop)

        self.scale = 1.0
        self.zooming = False
        self.start_x = 0
        self.start_y = 0

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Bitmap files", "*.bmp")])
        if file_path:
            self.image_path = file_path
            try:
                self.original_image = Image.open(self.image_path)
                self.display_image()   
            except Exception as e:
                messagebox.showerror("Erro", f"Nao foi possivel carregar a imagem:\n{str(e)}")

    def display_image(self):
        self.image = self.original_image.copy()
        self.tk_image = ImageTk.PhotoImage(self.image)
        image_width, image_height = self.image.size
        self.canvas.config(width=image_width, height=image_height, scrollregion=(0, 0, image_width, image_height))

        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        x_position = (canvas_width - image_width) // 2
        y_position = (canvas_height - image_height) // 2

        self.image_id = self.canvas.create_image(x_position, y_position, anchor=tk.NW, image=self.tk_image)
        self.show_path_button.config(state=tk.NORMAL)

    def show_path(self):
        source_pixel, destination_pixel = self.graph.build_graph(self.image_path)
        if source_pixel and destination_pixel:
            path = self.graph.path_bfs(source_pixel, destination_pixel)
            if path:
                drawn_path(path, self.image_path)
                self.original_image = Image.open("./Datasets/possible_path.bmp")
                self.display_image()
            else:
                messagebox.showerror("Nao ha caminho possivel.")
        else:
            messagebox.showerror("Pixel origem e/ou destino nao encontrados.")

    def on_key_press(self, event):
        if event.keysym == "plus":
            self.zoom_in()
        elif event.keysym == "minus":
            self.zoom_out()

    def on_key_release(self, event):
        pass

    def on_drag_start(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        self.canvas.move(self.image_id, delta_x, delta_y)
        self.start_x = event.x
        self.start_y = event.y

    def on_drag_stop(self, event):
        pass
