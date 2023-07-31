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
from tkinter import *
from tkinter import ttk
import matplotlib
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import main
import random
import threading


# ============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("Langton's ant")
        self.color = {0: "white", 1: "black", 2: "#742B22"}
        self.size = (20, 20)
        self.pixel_start = (75, 72)
        self.pixel_end = (540, 534)
        self.directions = [1, 2, 3, 4]
        self.matrix_rotation_right = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        self.matrix_rotation_left = np.array([[0, -1], [-1, 0], [0, 1], [1, 0]])
        self.data = np.full(self.size, 0, dtype=int)
        self.data_update = np.full(self.size, 0, dtype=int)
        self.thread_running = bool
        self.fig = matplotlib.figure.Figure
        self.ax = matplotlib.axes
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg

        # Create widgets
        self.start_game_of_life()

    def auto(self):
        self.plot()
        threading.Timer(0.5, self.auto).start()

    def plot(self):
        self.ax.clear()  # clear axes from previous plot
        self.update_plt()
        self.canvas.draw()

    def start_game_of_life(self):
        """
        start_game_of_life is the main script of game of life
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
                    if int(self.data[-y_location][x_location]) == 0:  # if the user clic on a white cell
                        rectangle = plt.Rectangle((x_location + 0.25, y_location + 0.25), 0.5, 0.5, fc=self.color[2])
                        self.data[-y_location][x_location] = random.choice(self.directions) * 10
                    elif int(self.data[-y_location][x_location]) == 1:  # if the user clic on a black cell
                        rectangle = plt.Rectangle((x_location + 0.25, y_location + 0.25), 0.5, 0.5, fc=self.color[2])
                        self.data[-y_location][x_location] = int(str(random.choice(self.directions)) + '1')
                    else:  # if the user clic on ant, clear the cell
                        rectangle = plt.Rectangle((x_location, y_location), 1, 1, fc=self.color[0])
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
        tk.mainloop()

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
    """

    def turn_right(self, x, y, direction_facing):
        self.data_update[x + self.matrix_rotation_right[direction_facing - 1][0]][
            y + self.matrix_rotation_right[direction_facing - 1][1]] = int(
            str(self.directions[direction_facing % 4]) + str(
                self.data_update[x + self.matrix_rotation_right[direction_facing - 1][0]]
                [y + self.matrix_rotation_right[direction_facing - 1][1]]))

    def turn_left(self, x, y, direction_facing):
        self.data_update[x + self.matrix_rotation_left[direction_facing - 1][0]][
            y + self.matrix_rotation_left[direction_facing - 1][1]] = int(
            str(self.directions[(direction_facing - 2) % 4]) + str(
                self.data_update[x + self.matrix_rotation_left[direction_facing - 1][0]]
                [y + self.matrix_rotation_left[direction_facing - 1][1]]))

    def update_data(self, x, y, state):
        if len(state) == 1:
            pass
        else:
            for i in range(len(state) - 1):
                if int(state[-1:]):  # turn to left
                    self.turn_left(x, y, int(state[i]))
                else:  # turn to right
                    self.turn_right(x, y, int(state[i]))
            if len(str(self.data[x][y])) != 1:
                if int(state[-1:]):
                    self.data_update[x][y] = int(str(self.data_update[x][y])[:-1] + '0')
                else:
                    self.data_update[x][y] = int(str(self.data_update[x][y])[:-1] + '1')
            else:
                if int(state[-1:]):
                    self.data_update[x][y] = 0
                else:
                    self.data_update[x][y] = 1

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
                rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.color[state])
                self.ax.add_patch(rectangle)
            else:
                rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.color[int(str(state)[-1:])])
                ant = plt.Rectangle((y + 0.25, -x + 0.25), 0.5, 0.5, fc=self.color[2])
                self.ax.add_patch(rectangle)
                self.ax.add_patch(ant)

        for (line, element), value in np.ndenumerate(self.data_update):  # first create the floor canvas
            # Iterate over the elements and their indices using np.ndenumerate
            self.data_update[line][element] = int(str(self.data[line][element])[-1:])
        for (line, element), value in np.ndenumerate(self.data):  # update the datas
            self.update_data(line, element, str(value))
        self.data = self.data_update
        for (line, element), value in np.ndenumerate(self.data):  # update the pixels of the canvas
            color_pixel(int(value), line, element)
        return self.data_update
