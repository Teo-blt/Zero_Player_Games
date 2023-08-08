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
import main
import random
import matplotlib
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from random import choice
from matplotlib import colors
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================================

class Creature:
    """A sea creature living in Wa-Tor world."""

    def __init__(self, id, x, y, init_energy, fertility_threshold, gender):
        """Initialize the creature.

        id is an integer identifying the creature.
        x, y is the creature's position in the Wa-Tor world grid.
        init_energy is the creature's initial energy: this decreases by 1
            each time the creature moves and if it reaches 0 the creature dies.
        fertility_threshold: each chronon, the creature's fertility increases
            by 1. When it reaches fertility_threshold, the creature reproduces.

        """

        self.id = id
        self.x, self.y = x, y
        self.energy = init_energy
        self.fertility_threshold = fertility_threshold
        self.gender = gender
        self.fertility = 0
        self.dead = False


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("WA-TOR")
        self.color = ["black", "green", "blue"]
        self.type_of_gender = ["male", "female"]  # I SPECIFY, WE ARE TALKING ABOUT FISH
        self.neighbor = ((0, -1), (1, 0), (0, 1), (-1, 0))
        self.creatures = []
        self.possible_movement = []
        self.no_pray_movement = []
        self.SEED = 10
        self.step = 0
        self.EMPTY = 0
        self.FISH = 1
        self.SHARK = 2
        self.nb_fish = 0
        self.nb_shark = 0
        self.size = (10, 10)
        self.pixel_start = (75, 72)
        self.pixel_end = (540, 534)
        self.initial_energies = {self.FISH: 20, self.SHARK: 3}
        self.fertility_thresholds = {self.FISH: 4, self.SHARK: 12}
        random.seed(self.SEED)
        self.data_for_ani = np.zeros(self.size, dtype=int)
        self.data = np.zeros(self.size, dtype=object)
        self.data_update = np.zeros(self.size, dtype=object)
        self.step_entry = ttk.Entry()
        self.fish_entry = ttk.Entry()
        self.shark_entry = ttk.Entry()
        self.fig = matplotlib.figure.Figure
        self.ax = matplotlib.axes
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg

        # Animation settings
        self.paused = 1
        self.interval = 100
        self.im = matplotlib.image.AxesImage
        self.anim = animation.FuncAnimation
        self.cmap = colors.ListedColormap(self.color)  # ["black", "green", "blue"]
        self.norm = colors.BoundaryNorm([0, 1, 2, 3], self.cmap.N)  # number of color HERE

        # Create widgets
        self.start_wa_tor()

    def animate(self, i: int):
        """
        animate is the animation function
        """
        if self.paused:
            pass
        else:
            self.upload_entry()
            self.im.set_data(self.good_ani_format())
            self.data = self.update_data()

    def good_ani_format(self):
        """
        good_ani_format is a function to extract only the id of the data matrix
        """
        self.data_for_ani = np.zeros(self.size, dtype=int)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if type(self.data[i, j]) == int:
                    pass
                else:
                    self.data_for_ani[i, j] = self.data[i, j].id
        return self.data_for_ani

    def plot(self):
        """
        plot is a function to advance of one step in the simulation
        """
        self.data = self.update_data()
        self.upload_entry()
        self.im.set_data(self.good_ani_format())
        print(self.data)

    def upload_entry(self):
        """
        upload_entry is a function to add + 1 to the step counter
        """
        self.step -= -1
        self.step_entry.delete(0, 2000)
        self.step_entry.insert(0, "Step : " + str(self.step))
        self.fish_entry.delete(0, 2000)
        self.fish_entry.insert(0, "Number of fish : " + str(self.nb_fish))
        self.shark_entry.delete(0, 2000)
        self.shark_entry.insert(0, "Number of shark : " + str(self.nb_shark))

    def toggle_pause(self):
        """
        toggle_pause is a function to start/stop the animation
        """
        self.paused = not self.paused

    def start_wa_tor(self):
        """
        start_wa_tor is the main script of WA-TOR
        """
        matplotlib.use("TkAgg")
        self.wm_title("WA-TOR")
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
        toggle_pause_button = ttk.Button(menu_frame, text="Toggle pause", cursor="right_ptr",
                                         command=lambda: [self.toggle_pause()])
        toggle_pause_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        self.step_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.step_entry.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.fish_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.fish_entry.grid(row=4, column=0, padx=5, pady=10, sticky="ew")
        self.shark_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.shark_entry.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

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
                        if type(self.data[-y_location][x_location]) == int:
                            self.spawn_creature((self.data[-y_location][x_location] + 1) % len(self.color),
                                                x_location, y_location)
                        else:
                            self.destroy_creature(x_location, y_location)
                            self.spawn_creature((self.data[-y_location][x_location].id + 1) % len(self.color),
                                                x_location, y_location)
                        self.im.set_data(self.good_ani_format())

        def link_to_f_not_motion(event: Event):
            f(event, 0)

        def link_to_f_motion(event: Event):
            f(event, 1)

        self.upload_entry()
        self.bind("<Button-1>", link_to_f_not_motion)
        self.bind("<B1-Motion>", link_to_f_motion)
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")

        self.im = self.ax.imshow(self.data_for_ani, cmap=self.cmap, norm=self.norm)
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=self.interval, frames=200)
        tk.mainloop()

    def destroy_creature(self, x: int, y: int):
        """
        destroy_creature remove a creature from the creatures list

        :param x: x position of the creature to destroy
        :param y: y position of the creature to destroy
        """
        self.creatures.remove(self.data[-y][x])

    def spawn_creature(self, creature_id: int, x: int, y: int):
        """
        spawn_creature Spawn a creature of type ID creature_id at location x,y

        :param creature_id: type of creature to spawn
        :param x: x position of the creature to spawn
        :param y: y position of the creature to spawn
        """
        if creature_id == self.EMPTY:
            self.data[-y][x] = self.EMPTY
        else:
            creature = Creature(creature_id, x, y,
                                self.initial_energies[creature_id],
                                self.fertility_thresholds[creature_id],
                                choice(self.type_of_gender))
            self.creatures.append(creature)
            self.data[-y][x] = creature

    def update_data(self):
        """
        update_data is a function that update the data to one step
        """
        # Shuffle the creatures grid so that we don't always evolve the same
        # creatures first.
        random.shuffle(self.creatures)

        # NB The self.creatures list is going to grow as new creatures are
        # spawned, so loop over indices into the list as it stands now.
        n_creatures = len(self.creatures)
        self.nb_fish = 0
        self.nb_shark = 0
        for i in range(n_creatures):
            creature = self.creatures[i]
            if creature.dead:
                # This creature has been eaten so skip it.
                continue
            if creature.id == self.SHARK:
                self.nb_shark += 1
            else:
                self.nb_fish += 1
            self.detect_neighbor(creature, -creature.y, creature.x)
            self.move(creature, -creature.y, creature.x)
            self.loose_energy(creature)
            self.reproduce(creature)
        self.remove_dead()
        return self.data_update

    def detect_neighbor(self, the_creature, position_x: int, position_y: int):
        """
        detect_neighbor is a function that detect all the neighbor

        :param the_creature: class Creature
        :param position_x: x position of the creature to move
        :param position_y: y position of the creature to move
        """
        self.possible_movement = []
        self.no_pray_movement = []
        for dx, dy in self.neighbor:
            if (position_x + dx >= self.size[0] or position_x + dx < 0 or position_y + dy >= self.size[1]
                    or position_y + dy < 0):  # check if it is out of limits
                continue
            if the_creature.id == self.FISH:
                if self.data[position_x + dx, position_y + dy] == self.EMPTY:
                    self.possible_movement.append((dx, dy))
            else:
                if self.data[position_x + dx, position_y + dy] == self.EMPTY:
                    self.no_pray_movement.append((dx, dy))
                else:
                    if self.data[position_x + dx, position_y + dy].id == self.FISH:
                        self.possible_movement.append((dx, dy))

    def move(self, the_creature, position_x: int, position_y: int):
        """
        move is a function that move a creature of one step

        :param the_creature: class Creature
        :param position_x: x position of the creature to move
        :param position_y: y position of the creature to move
        """

        if the_creature.id == self.FISH:
            if len(self.possible_movement) != 0:
                (x, y) = choice(self.possible_movement)
                self.data_update[position_x, position_y] = 0
                self.data_update[position_x + x, position_y + y] = the_creature
                the_creature.x += y
                the_creature.y -= x
            else:
                self.data_update[position_x, position_y] = the_creature
        elif the_creature.id == self.SHARK:
            if len(self.possible_movement) != 0:
                (x, y) = choice(self.possible_movement)
                self.data_update[position_x, position_y] = 0
                self.data_update[position_x + x, position_y + y] = the_creature
                the_creature.x += y
                the_creature.y -= x
            else:
                if len(self.no_pray_movement) != 0:
                    (x, y) = choice(self.no_pray_movement)
                    self.data_update[position_x, position_y] = 0
                    self.data_update[position_x + x, position_y + y] = the_creature
                    the_creature.x += y
                    the_creature.y -= x
                else:
                    self.data_update[position_x, position_y] = the_creature

    def loose_energy(self, the_creature):
        """
        loose_energy is a function that remove energy of the concerned creatures

        :param the_creature: class Creature
        """
        if the_creature.id == self.SHARK:
            the_creature.energy -= 1
            if the_creature.energy < 0:
                the_creature.dead = True

    def reproduce(self, the_creature):
        """
        reproduce is a function that reproduce the selected creature

        :param the_creature: class Creature
        """
        the_creature.fertility += 1
        if the_creature.fertility >= the_creature.fertility_threshold:
            the_creature.fertility = 0

    def remove_dead(self):
        for creature in self.creatures:
            if creature.dead:
                self.destroy_creature(creature.x, creature.y)
                self.data[-creature.y][creature.x] = 0


if __name__ == "__main__":
    # execute only if run as a script
    Application().mainloop()
