import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GridOfPixels:
    def __init__(self, canvas_size=(5, 5), rules=None):
        self.canvas_size = canvas_size
        self.rules = rules if rules else {0: ("white",), 1: ("red",), 2: ("blue",)}

    def draw_pixel(self, canvas, state, x, y):
        color = self.rules.get(int(str(state)[-1:]), ("white",))[0]

        fig = Figure(figsize=(1, 1), facecolor=color)
        pixel_canvas = FigureCanvasTkAgg(fig, master=canvas)
        pixel_canvas.draw()

        pixel_canvas.get_tk_widget().grid(row=x, column=y)

def main():
    # Define the grid size
    rows, cols = 5, 5

    # Create the main application window
    root = tk.Tk()
    root.title("Grid of Pixels")

    # Create the canvas to draw the grid of pixels
    canvas = tk.Canvas(root)
    canvas.pack()

    # Create an instance of GridOfPixels
    grid_of_pixels = GridOfPixels(canvas_size=(rows, cols))

    # Example: Drawing pixels in different positions with different states
    grid_of_pixels.draw_pixel(canvas, 1, 0, 0)  # State 1 (Red) at position (0, 0)
    grid_of_pixels.draw_pixel(canvas, 2, 1, 1)  # State 2 (Blue) at position (1, 1)
    grid_of_pixels.draw_pixel(canvas, 11, 2, 2)  # State 1 (Red) at position (2, 2) with an ant (brown)

    # Run the main Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()