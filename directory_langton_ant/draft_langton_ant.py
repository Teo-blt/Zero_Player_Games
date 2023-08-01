#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 20 16:30:00 2023
# For Wi6labs, all rights reserved
# =============================================================================
"""The Module Has Been Build try zero player games"""
# =============================================================================
# Imports

import matplotlib
import main
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from random import choice
from threading import Timer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from matplotlib.figure import Figure


# ============================================================================


class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("Langton's ant")
        self.rules = [["white", "L"], ["black", "L"], ["Blue", "R"], ["Red", "R"]]
        self.step = 0
        self.show = 1
        self.size = (20, 20)
        self.pixel_start = (75, 72)  # top left pixel
        self.pixel_end = (540, 534)  # bottom right pixel
        self.directions = [1, 2, 3, 4]  # [North : 1, East : 2, South : 3, West : 4]
        self.matrix_rotation_right = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])  # turn to right
        self.matrix_rotation_left = np.array([[0, -1], [-1, 0], [0, 1], [1, 0]])  # turn to left
        self.data = np.full(self.size, 0, dtype=int)
        self.data_update = np.full(self.size, 0, dtype=int)
        self.step_entry = ttk.Entry()
        self.fig = matplotlib.figure.Figure
        self.ax = matplotlib.axes
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg

        # Create widgets
        self.start_langton_ant()

    def auto(self):
        """
        plot is a function that automatically call plot to update the simulation
        """
        start_time = time.time()
        self.plot()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function execution time: {execution_time:.6f} seconds")
        Timer(0.001, self.auto).start()

    def plot(self):
        """
        plot is a function that update the simulation of one step
        """
        self.upload_entry()
        self.ax.clear()  # clear axes from previous plot
        self.data = self.update_plt()
        self.canvas.draw()

    def upload_entry(self):
        self.step -= -1
        self.step_entry.delete(0, 2000)
        self.step_entry.insert(0, "Step : " + str(self.step))

    def switch(self):
        self.show += 1
        if self.show == 2:
            self.show = 0

    def start_langton_ant(self):
        """
        start_langton_ant is the main script of game of life
        """
        matplotlib.use('TkAgg')
        self.wm_title("Langton's ant")
        self.geometry("800x600")
        self.fig = plt.Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        menu_frame = ttk.LabelFrame(self, text="Menu")
        menu_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        plot_button = ttk.Button(menu_frame, text="Plot", cursor="right_ptr",
                                 command=lambda: [self.plot()])
        plot_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        back_button = ttk.Button(menu_frame, text="Back", cursor="right_ptr",
                                 command=lambda: [main.Application().mainloop()])
        back_button.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        auto_button = ttk.Button(menu_frame, text="Auto", cursor="right_ptr",
                                 command=lambda: [self.auto()])
        auto_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        show_button = ttk.Button(menu_frame, text="Faster", cursor="right_ptr",
                                 command=lambda: [self.switch()])
        show_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.step_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.step_entry.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        def f(event: Event):
            """
            f is a function that allow the user to create ants on the canvas with a clik

            :param event: information about the clic of the user (position and more)
            """
            if event.x <= self.pixel_start[0] or event.y <= self.pixel_start[1] or \
                    event.x >= self.pixel_end[0] or event.y >= self.pixel_end[1]:  # check if  off limits
                pass
            else:
                # do not use int() for x_pixel et y_pixel
                x_pixel = (self.pixel_end[0] - self.pixel_start[0]) / self.size[0]  # x length of a pixel
                y_pixel = (self.pixel_end[1] - self.pixel_start[1]) / self.size[1]  # y length of a pixel
                x_location = int((event.x - self.pixel_start[0]) / x_pixel)  # x position on the canvas
                y_location = -(int((event.y - self.pixel_start[1]) / y_pixel))  # y position on the canvas
                if int(x_location) >= self.size[0] or int(y_location) > 0 or \
                        int(x_location) < 0 or int(y_location) <= -self.size[1]:  # check if  off limits
                    pass
                else:
                    if len(str(self.data[-y_location][x_location])) == 1:  # if the user clic on an empty cell
                        rectangle = plt.Rectangle((x_location + 0.25, y_location + 0.25), 0.5, 0.5, fc="#742B22")
                        self.data[-y_location][x_location] = int(str(choice(self.directions)) + str(
                            (self.data[-y_location][x_location] % len(self.rules))))
                    else:
                        rectangle = plt.Rectangle((x_location, y_location), 1, 1, fc=self.rules[0][0])
                        self.data[-y_location][x_location] = 0
                    self.ax.add_patch(rectangle)
                    self.canvas.draw()

        self.bind("<Button-1>", f)
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.ax.autoscale(enable=True, axis="x", tight=True)
        self.ax.autoscale(enable=True, axis="y", tight=True)
        self.update_plt()
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")
        mainloop()

    """
    what do we want about update data
    - if there is not ant, do nothing
    - if there is one (1) ant or more do the following:
        - in function of the color of the cell, the ant can do four (4) actions:
            - turn left L
            - turn right R 
            - continue straight ahead C 
            - turn 180° around U
        - the ant then proceed to change the color of the cell according to a cycle move one cell
    -----------------------------------------------------------------
    Basically, I can replace all the turn function by one big function, but I think there are already 
    complex to read enough
    -----------------------------------------------------------------
    """

    def turn_right(self, x: int, y: int, direction_facing: int):
        """
        turn_right is a function that turn an ant to the right

        :param x: x position of the pixel
        :param y: y position of the pixel
        :param direction_facing: information about the facing direction of the ant
        [North : 1, East : 2, South : 3, West : 4]
        """
        if self.out_of_bounds(x, y, direction_facing, self.matrix_rotation_right):
            pass
        else:
            self.data_update[x + self.matrix_rotation_right[direction_facing - 1][0]][
                y + self.matrix_rotation_right[direction_facing - 1][1]] = int(
                str(self.directions[direction_facing % 4]) + str(
                    self.data_update[x + self.matrix_rotation_right[direction_facing - 1][0]]
                    [y + self.matrix_rotation_right[direction_facing - 1][1]]))

    def turn_left(self, x: int, y: int, direction_facing: int):
        """
        turn_left is a function that turn an ant to the left

        :param x: x position of the pixel
        :param y: y position of the pixel
        :param direction_facing: information about the facing direction of the ant
        [North : 1, East : 2, South : 3, West : 4]
        """
        if self.out_of_bounds(x, y, direction_facing, self.matrix_rotation_left):
            pass
        else:
            self.data_update[x + self.matrix_rotation_left[direction_facing - 1][0]][
                y + self.matrix_rotation_left[direction_facing - 1][1]] = int(
                str(self.directions[(direction_facing - 2) % 4]) + str(
                    self.data_update[x + self.matrix_rotation_left[direction_facing - 1][0]]
                    [y + self.matrix_rotation_left[direction_facing - 1][1]]))

    def update_data(self, x: int, y: int, state: str):
        """
        update_data is a function that update the data to one step

        :param x: x position of the pixel
        :param y: y position of the pixel
        :param state: information about the facing direction of the ant [North : 1, East : 2, South : 3, West : 4]
        """
        if len(state) == 1:  # Pass the empty cells
            pass
        else:
            for i in range(len(state) - 1):
                match self.rules[int(state[-1:])][1]:
                    case "R":  # turn to right
                        self.turn_right(x, y, int(state[i]))
                    case "L":  # turn to left
                        self.turn_left(x, y, int(state[i]))
                    case "C":  # straight ahead
                        pass
                    case "U":  # turn 180° around
                        pass
                    case _:
                        print("error", int(state[-1:]))

            # change the color of the cell according to a cycle
            if len(str(self.data[x][y])) != 1:  # if there is at least one ant
                self.data_update[x][y] = int(str(self.data_update[x][y])[:-1] + str(
                    ((int(state[-1:]) + 1) % len(self.rules))))
            else:  # if the cell is empty
                self.data_update[x][y] = ((int(state[-1:]) + 1) % len(self.rules))

    def out_of_bounds(self, x: int, y: int, state: int, type_rotation: np.ndarray):
        """
        out_of_bounds is a function that calculate if the next step of the ant is out of bounds

        :param x: x position of the pixel
        :param y: y position of the pixel
        :param state: information about the facing direction of the ant [North : 1, East : 2, South : 3, West : 4]
        :param type_rotation: matrix of rotation

        :return bool: 1 if out of bounds else 0
        """
        if (x + type_rotation[state - 1][0] >= self.size[0] or x + type_rotation[state - 1][0] < 0 or y +
                type_rotation[state - 1][
                    1]
                >= self.size[1] or y + type_rotation[state - 1][1] < 0):
            return 1
        else:
            return 0

    def update_plt(self):
        """
        update_plt is a function that update the plot to the next step
        """
        self.data_update = np.full(self.size, 0, dtype=int)  # clear data_update
        self.ax.autoscale(enable=True, axis="x", tight=True)
        self.ax.autoscale(enable=True, axis="y", tight=True)

        def color_pixel(state: int, x: int, y: int):
            """
            color_pixel is a function that color a pixel in the canvas

            :param state: value to color
            :param x: x position of the pixel
            :param y: y position of the pixel

            :return self.data_update: the updated datas
            """
            if len(str(state)) == 1:  # if there is no ants
                rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.rules[state][0])
                self.ax.add_patch(rectangle)
            else:
                rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.rules[int(str(state)[-1:])][0])
                ant = plt.Rectangle((y + 0.25, -x + 0.25), 0.5, 0.5, fc="#742B22")
                self.ax.add_patch(rectangle)
                self.ax.add_patch(ant)

        for (line, element), value in np.ndenumerate(self.data_update):  # first create the floor canvas
            # Iterate over the elements and their indices using np.ndenumerate
            self.data_update[line][element] = int(str(self.data[line][element])[-1:])

        for (line, element), value in np.ndenumerate(self.data):  # update the datas
            self.update_data(line, element, str(value))

        if self.show:
            for (line, element), value in np.ndenumerate(self.data_update):  # update the pixels of the canvas TOO LONG
                color_pixel(int(value), line, element)

        return self.data_update


"""
def auto():
    start_time = time.time()
    function_test()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Function execution time: {execution_time:.6f} seconds")
    threading.Timer(0.5, auto).start()
"""

if __name__ == "__main__":
    # execute only if run as a script
    Application().mainloop()
