#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 20 16:30:00 2023
# For Wi6labs, all rights reserved
# =============================================================================
"""The Module Has Been Build try zero player games"""
import time
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


def random_direction():
    # {1: "N", 2: "E", 3: "S", 4: "W"}
    directions = [1, 2, 3, 4]
    return random.choice(directions)


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("Langton's ant")
        self.color = {0: "white", 1: "black", 2: "#742B22"}
        self.size = (20, 20)
        self.pixel_start = (75, 72)
        self.pixel_end = (540, 534)
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

        def f(event):
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
                    if int(self.data[-y_location][x_location]) == 0:
                        rectangle = plt.Rectangle((x_location + 0.25, y_location + 0.25), 0.5, 0.5, fc=self.color[2])
                        self.data[-y_location][x_location] = random_direction() * 10
                    elif int(self.data[-y_location][x_location]) == 1:
                        rectangle = plt.Rectangle((x_location + 0.25, y_location + 0.25), 0.5, 0.5, fc=self.color[2])
                        self.data[-y_location][x_location] = int(str(random_direction()) + '1')
                    else:
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

    def update_data(self, x, y, state):
        state = str(int(state))
        if state == '0' or state == '1':
            pass
        else:
            for i in range(len(state) - 1):
                match state[i]:
                    case '1':  # "N"
                        if int(state[-1:]):  # turn to left
                            if y - 1 < 0:
                                pass
                            else:
                                self.data_update[x][y - 1] = int('4' + str(self.data_update[x][y - 1]))
                        else:  # turn to right
                            if y + 1 >= self.size[1]:
                                pass
                            else:
                                self.data_update[x][y + 1] = int('2' + str(self.data_update[x][y + 1]))
                    case '2':  # "E"
                        if int(state[-1:]):  # turn to left
                            if x - 1 < 0:
                                pass
                            else:
                                self.data_update[x - 1][y] = int('1' + str(self.data_update[x - 1][y]))
                        else:  # turn to right
                            if x + 1 >= self.size[0]:
                                pass
                            else:
                                self.data_update[x + 1][y] = int('3' + str(self.data_update[x + 1][y]))
                    case '3':  # "S"
                        if int(state[-1:]):  # turn to left
                            if y + 1 >= self.size[1]:
                                pass
                            else:
                                self.data_update[x][y + 1] = int('2' + str(self.data_update[x][y + 1]))
                        else:  # turn to right
                            if y - 1 < 0:
                                pass
                            else:
                                self.data_update[x][y - 1] = int('4' + str(self.data_update[x][y - 1]))
                    case '4':  # "W"
                        if int(state[-1:]):  # turn to left
                            if x + 1 >= self.size[0]:
                                pass
                            else:
                                self.data_update[x + 1][y] = int('3' + str(self.data_update[x + 1][y]))
                        else:  # turn to right
                            if x - 1 < 0:
                                pass
                            else:
                                self.data_update[x - 1][y] = int('1' + str(self.data_update[x - 1][y]))
                    case _:
                        print('Error value', state)
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
        self.data_update = np.full(self.size, 0, dtype=int)
        self.ax.autoscale(enable=True, axis="x", tight=True)
        self.ax.autoscale(enable=True, axis="y", tight=True)

        def color_pixel(state, x, y):
            if state == 0 or state == 1:
                rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.color[state])
                self.ax.add_patch(rectangle)
            else:
                rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.color[int(str(state)[-1:])])
                ant = plt.Rectangle((y + 0.25, -x + 0.25), 0.5, 0.5, fc=self.color[2])
                self.ax.add_patch(rectangle)
                self.ax.add_patch(ant)

        for (line, element), value in np.ndenumerate(self.data_update):
            self.data_update[line][element] = int(str(self.data[line][element])[-1:])
        # Iterate over the elements and their indices using np.ndenumerate
        for (line, element), value in np.ndenumerate(self.data):
            self.update_data(line, element, value)
        self.data = self.data_update
        for (line, element), value in np.ndenumerate(self.data):
            color_pixel(int(value), line, element)
        return self.data_update


if __name__ == "__main__":
    # execute only if run as a script
    Application().mainloop()
