import matplotlib
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')
root = tk.Tk()
root.wm_title("Game of life")
root.geometry("800x600")
fig = plt.Figure(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=10, sticky="ew")
menu_frame = tk.LabelFrame(root, text="Menu")
menu_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
plot_button = tk.Button(menu_frame, text="Plot", cursor="right_ptr", command=lambda: [plot(canvas, ax)])
plot_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

color = {0: "white", 1: "black"}
size = (20, 20)
pixel_start = (75, 72)
pixel_end = (540, 534)
global data
global past_value
global data_update

data = np.zeros(size)
past_value = (2000, 2000)
data_update = np.zeros(size)


def f(event, movement):
    global data
    global past_value
    if event.x <= pixel_start[0] or event.y <= pixel_start[1] or \
            event.x >= pixel_end[0] or event.y >= pixel_end[1]:
        pass
    else:
        # do not use int() for x_pixel et y_pixel
        x_pixel = (pixel_end[0] - pixel_start[0]) / size[0]
        y_pixel = (pixel_end[1] - pixel_start[1]) / size[1]
        x_location = int((event.x - pixel_start[0]) / x_pixel)
        y_location = -(int((event.y - pixel_start[1]) / y_pixel))
        if int(x_location) >= size[0] or int(y_location) > 0 or \
                int(x_location) < 0 or int(y_location) <= -size[1]:
            pass
        else:
            if movement and past_value == (x_location, y_location):
                pass
            else:
                past_value = (x_location, y_location)
                if int(data[-y_location][x_location]):
                    rectangle = plt.Rectangle((x_location, y_location), 1, 1, fc=color[0])
                    data[-y_location][x_location] = 0
                else:
                    rectangle = plt.Rectangle((x_location, y_location), 1, 1, fc=color[1])
                    data[-y_location][x_location] = 1
                ax.add_patch(rectangle)
                canvas.draw()


def link_to_f_not_motion(event):
    f(event, 0)


def link_to_f_motion(event):
    f(event, 1)


root.bind("<Button-1>", link_to_f_not_motion)
root.bind("<B1-Motion>", link_to_f_motion)

ax = fig.add_subplot(111)
ax.autoscale(enable=True, axis="x", tight=True)
ax.autoscale(enable=True, axis="y", tight=True)
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)


def update_data(table, x, y):
    nb_neighbor = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if x + i < 0 or y + j < 0 or x + i > size[0] - 1 or y + j > size[1] - 1:
                pass
            elif i == 0 and j == 0:
                pass
            else:
                nb_neighbor += int(table[x + i, y + j])
    match nb_neighbor:
        case 0:
            data_update[x, y] = 0
        case 1:
            data_update[x, y] = 0
        case 2:
            if table[x, y]:
                data_update[x, y] = 1
            else:
                data_update[x, y] = 0
        case 3:
            data_update[x, y] = 1
        case 4:
            data_update[x, y] = 0
        case 5:
            data_update[x, y] = 0
        case 6:
            data_update[x, y] = 0
        case 7:
            data_update[x, y] = 0
        case 8:
            data_update[x, y] = 0
        case _:
            print('Error, number neighbor', nb_neighbor)


def update_plt(table):
    global data_update
    data_update = np.zeros(size)

    def color_pixel(state, x, y):
        rectangle = plt.Rectangle((y, -x), 1, 1, fc=color[state])
        ax.add_patch(rectangle)

    # Iterate over the elements and their indices using np.ndenumerate
    for (line, element), value in np.ndenumerate(table):
        update_data(table, line, element)
    table = data_update
    for (line, element), value in np.ndenumerate(table):
        color_pixel(value, line, element)
    return data_update


def plot(drawing, line):
    global data
    line.clear()  # clear axes from previous plot
    data = update_plt(data)
    line.autoscale(enable=True, axis="x", tight=True)
    line.autoscale(enable=True, axis="y", tight=True)
    drawing.draw()


data = update_plt(data)
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")
tk.mainloop()

