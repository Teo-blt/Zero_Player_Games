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
import threading


# ============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("Brian's Brain")
        self.color = {0: "white", 1: "black", 2: "red"}
        self.size = (20, 20)
        self.pixel_start = (75, 72)
        self.pixel_end = (540, 534)
        self.past_value = (2000, 2000)
        self.data = np.zeros(self.size)
        self.data_update = np.zeros(self.size)
        self.fig = matplotlib.figure.Figure
        self.ax = matplotlib.axes
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg

        # Create widgets
        self.start_brian_brain()

    def foo(self):
        self.plot()
        threading.Timer(0.25, self.foo).start()

    def plot(self):
        self.ax.clear()  # clear axes from previous plot
        self.update_plt()
        self.canvas.draw()

    def start_brian_brain(self):
        """
        start_game_of_life is the main script of game of life
        """
        matplotlib.use('TkAgg')
        self.wm_title("Brian's Brain")
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
        back_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        auto_button = ttk.Button(menu_frame, text="Auto", cursor="right_ptr",
                                 command=lambda: [self.foo()])
        auto_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        def f(event, movement):
            if event.x <= self.pixel_start[0] or event.y <= self.pixel_start[1] or \
                    event.x >= self.pixel_end[0] or event.y >= self.pixel_end[1]:
                pass
            else:
                # do not use int() for x_pixel et y_pixel
                x_pixel = (self.pixel_end[0] - self.pixel_start[0]) / self.size[0]
                y_pixel = (self.pixel_end[1] - self.pixel_start[1]) / self.size[1]
                x_location = int((event.x - self.pixel_start[0]) / x_pixel)
                y_location = -(int((event.y - self.pixel_start[1]) / y_pixel))
                if int(x_location) >= self.size[0] or int(y_location) > 0 or \
                        int(x_location) < 0 or int(y_location) <= -self.size[1]:
                    pass
                else:
                    if movement and self.past_value == (x_location, y_location):
                        pass
                    else:
                        self.past_value = (x_location, y_location)
                        if int(self.data[-y_location][x_location]):
                            rectangle = plt.Rectangle((x_location, y_location), 1, 1, fc=self.color[0])
                            self.data[-y_location][x_location] = 0
                        else:
                            rectangle = plt.Rectangle((x_location, y_location), 1, 1, fc=self.color[1])
                            self.data[-y_location][x_location] = 1
                        self.ax.add_patch(rectangle)
                        self.canvas.draw()

        def link_to_f_not_motion(event):
            f(event, 0)

        def link_to_f_motion(event):
            f(event, 1)

        self.bind("<Button-1>", link_to_f_not_motion)
        self.bind("<B1-Motion>", link_to_f_motion)
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.update_plt()
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")
        tk.mainloop()

    def update_data(self, x, y):
        nb_neighbor = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if x + i < 0 or y + j < 0 or x + i > self.size[0] - 1 or y + j > self.size[1] - 1:
                    pass
                elif i == 0 and j == 0:
                    pass
                else:
                    if self.data[x + i, y + j]:
                        nb_neighbor += 1
        if self.data[x, y] == 2:
            self.data_update[x, y] = 0
        if self.data[x, y] == 1:
            self.data_update[x, y] = 2
        if self.data[x, y] == 0 and nb_neighbor == 2:
            self.data_update[x, y] = 1

    def update_plt(self):
        """
        update_plt update the canvas and the data
        """
        self.data_update = np.zeros(self.size)
        self.ax.autoscale(enable=True, axis="x", tight=True)
        self.ax.autoscale(enable=True, axis="y", tight=True)

        def color_pixel(state, x, y):
            """
            color_pixel update the canvas and the data

            :param state: the value of the pixel (2 dying, 1 on, 0 off)
            :param x: x coordinate of the pixel
            :param y: y coordinate of the pixel
            :return: self.data_update the updated datas
            """
            rectangle = plt.Rectangle((y, -x), 1, 1, fc=self.color[state])
            self.ax.add_patch(rectangle)

        # Iterate over the elements and their indices using np.ndenumerate
        for (line, element), value in np.ndenumerate(self.data):
            self.update_data(line, element)
        self.data = self.data_update
        for (line, element), value in np.ndenumerate(self.data):
            color_pixel(value, line, element)