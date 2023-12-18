import tkinter
from interface import ImageViewer

# Creating window.
window = tkinter.Tk()

window.title("Image Viewer")
app = ImageViewer(master=window)

app.mainloop()
