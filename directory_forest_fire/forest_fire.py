#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: August 2 11:30:00 2023
# For Zero_player_game, all rights reserved
# =============================================================================
"""The Module Has Been Build try zero player games"""
# =============================================================================
# Imports
import matplotlib
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from random import random
from matplotlib import colors
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("Forest Fire")
        self.color = [(0.2, 0, 0), "green", "orange"]
        self.step = 0
        self.EMPTY = 0
        self.TREE = 1
        self.FIRE = 2
        self.probability_spontaneous_ignition = 0.001
        self.probability_diagonally_ignition = 0.573
        self.probability_ignition = 0.9
        self.probability_spawn = 0.05
        self.size = (20, 20)
        self.pixel_start = (75, 72)
        self.pixel_end = (540, 534)
        self.data = np.zeros(self.size)
        self.data_update = np.zeros(self.size)
        self.step_entry = ttk.Entry()
        self.fig = matplotlib.figure.Figure
        self.ax = matplotlib.axes
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg

        # Animation settings
        self.paused = 1
        self.interval = 100
        self.im = matplotlib.image.AxesImage
        self.anim = animation.FuncAnimation
        self.cmap = colors.ListedColormap(self.color)  # [(0.2, 0, 0), "green", "orange"]
        self.norm = colors.BoundaryNorm([0, 1, 2, 3], self.cmap.N)

        # Create widgets
        self.start_forest_fire()

    def animate(self, i: int):
        """
        animate is the animation function
        """
        if self.paused:
            pass
        else:
            self.upload_entry()
            self.im.set_data(self.data)
            self.data = self.update_data()

    def plot(self):
        """
        plot is a function to advance of one step in the simulation
        """
        self.upload_entry()
        self.data = self.update_data()
        self.im.set_data(self.data)

    def upload_entry(self):
        """
        upload_entry is a function to add + 1 to the step counter
        """
        self.step -= -1
        self.step_entry.delete(0, 2000)
        self.step_entry.insert(0, "Step : " + str(self.step))

    def toggle_pause(self):
        """
        toggle_pause is a function to start/stop the animation
        """
        self.paused = not self.paused

    def start_forest_fire(self):
        """
        start_forest_fire is the main script of Forest fire
        """
        matplotlib.use('TkAgg')
        self.wm_title("Forest Fire")
        self.geometry("800x600")
        self.fig = plt.Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        menu_frame = ttk.LabelFrame(self, text="Menu")
        menu_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        plot_button = ttk.Button(menu_frame, text="Plot", cursor="right_ptr",
                                 command=lambda: [self.plot()])
        plot_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        toggle_pause_button = ttk.Button(menu_frame, text="Toggle pause", cursor="right_ptr",
                                         command=lambda: [self.toggle_pause()])
        toggle_pause_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        self.step_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.step_entry.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        def f(event: Event, movement: int):
            """
            f is a function that allow the user to create ants on the canvas with a clik

            :param event: information about the clic of the user (position and more)
            :param movement: information about the movement of the mouse
            """
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
                    if movement == 1 and self.past_value == (x_location, y_location):
                        pass
                    else:
                        self.past_value = (x_location, y_location)
                        self.data[-y_location][x_location] = (self.data[-y_location][x_location] + 1) % len(self.color)
                        self.im.set_data(self.data)

        def link_to_f_not_motion(event):
            f(event, 0)

        def link_to_f_motion(event):
            f(event, 1)

        self.bind("<Button-1>", link_to_f_not_motion)
        self.bind("<B1-Motion>", link_to_f_motion)
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")

        self.im = self.ax.imshow(self.data, cmap=self.cmap, norm=self.norm)
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=self.interval, frames=200)
        tk.mainloop()

    def update_data(self):
        """
        update_data is a function that update the data to one step
        """
        self.data_update = np.zeros(self.size)
        for (x, y), value in np.ndenumerate(self.data):
            # (2 burning, 1 three, 0 empty)
            if self.data[x, y] == self.TREE:
                self.data_update[x, y] = self.TREE
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if x + i < 0 or y + j < 0 or x + i > self.size[0] - 1 or y + j > self.size[1] - 1:
                            continue
                        elif i == 0 and j == 0:
                            continue
                        # The diagonally-adjacent trees are further away, so
                        # only catch fire with a reduced probability:
                        elif abs(i) == abs(j) and random() < self.probability_diagonally_ignition:
                            continue
                        else:
                            if self.data[x + i, y + j] == self.FIRE:
                                self.data_update[x, y] = self.FIRE
                                break
                if random() <= self.probability_spontaneous_ignition:
                    self.data_update[x, y] = self.FIRE
            if self.data[x, y] == self.EMPTY:
                if random() <= self.probability_spawn:
                    self.data_update[x, y] = self.TREE
        return self.data_update

