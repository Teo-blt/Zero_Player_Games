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
from directory_wa_tor import drawing
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================================

class Creature:
    """
    a sea creature living in Wa-Tor world
    """

    def __init__(self, id: int, x: int, y: int, init_energy: int, fertility_threshold: int, gender: str):
        """
        initialize the creature

        :param id: is an integer identifying the creature
        :param x, y: is the creature's position in the Wa-Tor world grid
        :param init_energy: is the creature's initial energy: this decreases by 1
            each time the creature moves and if it reaches 0 the creature dies
        :param fertility_threshold: each step, the creature's fertility increases
            by 1. When it reaches fertility_threshold, the creature reproduces
        :param gender: only use when sexual reproduction is active,
            determine the gender of the creature
        """

        self.id = id
        self.x, self.y = x, y
        self.energy = init_energy
        self.fertility_threshold = fertility_threshold
        self.gender = gender
        self.fertility = 0
        self.dead = False


class Application(Tk):
    """
    the main Tk application
    """
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("WA-TOR")
        self.color = ["black", "green", "blue"]  # color of the creatures
        self.type_of_gender = ["male", "female"]  # I SPECIFY, WE ARE TALKING ABOUT FISH
        self.neighbor = ((0, -1), (1, 0), (0, 1), (-1, 0))  # The touching neighbor
        self.creatures = []  # list of all creatures
        self.primary_movement = []  # list of all primary possible movement for one creature at one moment
        self.secondary_movement = []  # list of all secondary possible movement for one creature at one moment
        self.number_fish_for_graph = []  # list with the population of fish at each time
        self.number_shark_for_graph = []  # list with the population of shark at each time
        self.moved = False  # if the selected creature have moved
        self.previous_position = 0, 0  # the position of the creature before moving
        self.SEED = 10  # for the random seed generation
        self.step = 0  # step of the simulation
        self.EMPTY = 0  # empty cell
        self.FISH = 1  # fish cell
        self.SHARK = 2  # shark cell
        self.nb_fish = 0  # population of fish
        self.nb_shark = 0  # population of shark
        self.size = (50, 50)  # size of the map
        self.pixel_start = (75, 72)  # the position of the starting pixel of the map (do not touch)
        self.pixel_end = (540, 534)  # the position of the ending pixel of the map (do not touch)
        self.use_sex = 0  # DO YOU WANT SEX ? (for activate sexual reproduction)
        self.initial_energies = {self.FISH: 20, self.SHARK: 3}  # starting energy of the species
        self.fertility_thresholds = {self.FISH: 4, self.SHARK: 12}  # fertility thresholds of the species
        random.seed(self.SEED)  # to randomize the random with the chosen seed
        self.data_for_ani = np.zeros(self.size, dtype=int)  # matrix for the animation (only the id of creature)
        self.data = np.zeros(self.size, dtype=object)  # matrix 3D with Creature
        self.step_entry = ttk.Entry()  # to show the number of step in the HMI
        self.fish_entry = ttk.Entry()  # to show the number of fish in the HMI
        self.shark_entry = ttk.Entry()  # to show the number of shark in the HMI

        # Canvas settings
        self.fig = matplotlib.figure.Figure
        self.ax = matplotlib.axes
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg

        # Animation settings
        self.paused = 1  # to pause the animation
        self.interval = 100  # interval between actualisation in ms
        self.im = matplotlib.image.AxesImage
        self.anim = animation.FuncAnimation
        self.cmap = colors.ListedColormap(self.color)  # ["black", "green", "blue"]
        self.norm = colors.BoundaryNorm([0, 1, 2, 3], self.cmap.N)  # number of color HERE
        # it's like :
        # between 0 and 1 it's black
        # between 1 and 2 it's green
        # between 2 and 3 it's blue

        # Create widgets
        self.start_wa_tor()

    def animate(self, i: int):
        """
        animate is the animation function
        """
        if self.paused:
            pass
        else:
            self.upload_entry()  # update the number of step/fish/shark in the HMI
            self.im.set_data(self.good_ani_format())  # update the animation
            self.update_data()  # update the data (self.data)

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
        return self.data_for_ani  # only the id of the self.data matrix

    def plot(self):
        """
        plot is a function to advance of one step in the simulation
        """
        self.update_data()  # update the data (self.data)
        self.upload_entry()  # update the number of step/fish/shark in the HMI
        self.im.set_data(self.good_ani_format())  # update the animation

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
        toggle_pause_button = ttk.Button(menu_frame, text="Toggle pause", cursor="right_ptr",
                                         command=lambda: [self.toggle_pause()])
        toggle_pause_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        draw_graph_button = ttk.Button(menu_frame, text="Draw graph", cursor="right_ptr",
                                       command=lambda: [drawing.Application(self.number_fish_for_graph,
                                                                            self.number_shark_for_graph)])
        draw_graph_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.step_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.step_entry.grid(row=4, column=0, padx=5, pady=10, sticky="ew")
        self.fish_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.fish_entry.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.shark_entry = ttk.Entry(menu_frame, cursor="right_ptr")
        self.shark_entry.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        def f(event: Event, movement: int):
            """
            f is a function that allow the user to create a cell on the canvas with a clik

            :param event: information about the clic of the user (position and more)
            :param movement: information about the movement of the mouse
            """
            if event.x <= self.pixel_start[0] or event.y <= self.pixel_start[1] or \
                    event.x >= self.pixel_end[0] or event.y >= self.pixel_end[1]:  # check if the clic is out-bound
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
                    if movement == 1 and self.past_value == (x_location, y_location):  # to prevent the cell from
                        # changing is state multiple time while the cursor of the user is still on the same cell
                        pass
                    else:
                        self.past_value = (x_location, y_location)
                        if type(self.data[-y_location][x_location]) == int:  # if it's a EMPTY cell
                            self.spawn_creature((self.data[-y_location][x_location] + 1) % len(self.color),
                                                x_location, y_location)
                        else:
                            self.creatures.remove(self.data[-y_location][x_location])
                            self.spawn_creature((self.data[-y_location][x_location].id + 1) % len(self.color),
                                                x_location, y_location)
                        self.im.set_data(self.good_ani_format())

        def link_to_f_not_motion(event: Event):
            f(event, 0)

        def link_to_f_motion(event: Event):
            f(event, 1)

        self.upload_entry()
        self.bind("<Button-1>", link_to_f_not_motion)  # place only one pixel
        self.bind("<B1-Motion>", link_to_f_motion)  # to allow the user to draw on the canvas
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")

        self.im = self.ax.imshow(self.data_for_ani, cmap=self.cmap, norm=self.norm)
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=self.interval, frames=200)
        tk.mainloop()

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
            choice([-1, 0, 1])  # to randomize (a little) the fertility of the creature
            creature = Creature(creature_id, x, y,
                                self.initial_energies[creature_id],
                                self.fertility_thresholds[creature_id] + choice([-1, 0, 1]),
                                choice(self.type_of_gender))
            self.creatures.append(creature)
            self.data[-y][x] = creature

    def update_data(self):
        """
        update_data is a function that update the data to one step
        """
        # shuffle the creatures grid so that we don't always evolve the same creatures first
        random.shuffle(self.creatures)

        # the self.creatures list is going to grow as new creatures are spawned, so loop over indices into
        # the list as it stands now
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
            self.detect_neighbor(creature, -creature.y, creature.x)  # look for neighbor
            self.move(creature, -creature.y, creature.x)  # move and eat
            self.loose_energy(creature)  # loose energy
            self.reproduce(creature)  # reproduce (maybe)
        self.number_fish_for_graph.append(self.nb_fish)
        self.number_shark_for_graph.append(self.nb_shark)
        self.remove_dead()

    def detect_neighbor(self, the_creature: Creature, position_x: int, position_y: int):
        """
        detect_neighbor is a function that detect all the neighbor

        :param the_creature: class Creature
        :param position_x: x position of the creature to move
        :param position_y: y position of the creature to move
        """
        self.primary_movement = []
        self.secondary_movement = []
        for dx, dy in self.neighbor:
            if the_creature.id == self.FISH:  # if it's a fish, only look for empty cells
                if self.data[(position_x + dx) % self.size[0], (position_y + dy) % self.size[1]] == self.EMPTY:
                    self.primary_movement.append(((position_y + dy) % self.size[1], (position_x + dx) % self.size[0]))
            else:  # if it's a shark, look for prey in priority
                if self.data[(position_x + dx) % self.size[0], (position_y + dy) % self.size[1]] == self.EMPTY:
                    self.secondary_movement.append(((position_y + dy) % self.size[1], (position_x + dx) % self.size[0]))
                else:
                    if self.data[(position_x + dx) % self.size[0], (position_y + dy) % self.size[1]].id == self.FISH:
                        self.primary_movement.append(
                            ((position_y + dy) % self.size[1], (position_x + dx) % self.size[0]))

    def move(self, the_creature: Creature, position_x: int, position_y: int):
        """
        move is a function that move a creature of one step

        :param the_creature: class Creature
        :param position_x: x position of the creature to move
        :param position_y: y position of the creature to move
        """
        self.moved = False

        def the_moving_action(i_can_eat: bool):
            """
            the_moving_action is a function that move a creature of one step

            :param i_can_eat:
            """
            if len(self.primary_movement) == 0:  # if no primary movement possible look for secondary movement
                if len(self.secondary_movement) == 0:  # if no secondary movement
                    self.data[position_x, position_y] = the_creature  # do not move
                else:
                    self.primary_movement = self.secondary_movement  # secondary movement become primary movement
            (x, y) = choice(self.primary_movement)
            self.previous_position = position_x, position_y
            self.data[position_x, position_y] = 0
            if i_can_eat:  # if the creature are able to eat
                self.data[y, x].dead = True  # eat the creature
                the_creature.energy += 2
            self.data[y, x] = the_creature
            the_creature.x, the_creature.y = x, -y
            self.moved = True

        if the_creature.id == self.FISH:
            the_moving_action(False)
        elif the_creature.id == self.SHARK:
            the_moving_action(True)

    def loose_energy(self, the_creature: Creature):
        """
        loose_energy is a function that remove energy of the concerned creatures

        :param the_creature: class Creature
        """
        the_creature.energy -= 1
        if the_creature.energy < 0:
            the_creature.dead = True
            if the_creature.id == self.SHARK:
                self.nb_shark -= 1
            elif the_creature.id == self.FISH:
                self.nb_fish -= 1

    def reproduce(self, the_creature: Creature):
        """
        reproduce is a function that reproduce the selected creature

        :param the_creature: class Creature
        """
        if self.use_sex:  # If we use the sexual reproduction
            the_creature.fertility += 1
            if the_creature.fertility >= the_creature.fertility_threshold and self.moved:
                for dx, dy in self.neighbor:
                    if self.data[(the_creature.x + dx) % self.size[0], (the_creature.y + dy) % self.size[1]] == 0:
                        continue
                    elif self.data[(the_creature.x + dx) % self.size[0], (the_creature.y + dy) % self.size[
                        1]].id == the_creature.id and self.data[
                        (the_creature.x + dx) % self.size[0], (the_creature.y + dy) % self.size[
                            1]].gender != the_creature.gender and self.data[
                        (the_creature.x + dx) % self.size[0], (the_creature.y + dy) % self.size[1]].fertility >= \
                            self.data[(the_creature.x + dx) % self.size[0], (the_creature.y + dy) % self.size[
                                1]].fertility_threshold:
                        # we are cheking if the creature have neighbor from the same species, from a different gender
                        # and if the neighbor creature have reach the fertility threshold
                        the_creature.fertility = 0
                        self.data[
                            (the_creature.x + dx) % self.size[0], (the_creature.y + dy) % self.size[1]].fertility = 0
                        self.spawn_creature(the_creature.id, self.previous_position[1], -self.previous_position[0])
                        if the_creature.id == self.SHARK:
                            self.nb_shark += 1
                        elif the_creature.id == self.FISH:
                            self.nb_fish += 1
        else:  # If we use the clone reproduction
            the_creature.fertility += 1
            if the_creature.fertility >= the_creature.fertility_threshold and self.moved:
                the_creature.fertility = 0
                self.spawn_creature(the_creature.id, self.previous_position[1], -self.previous_position[0])
                if the_creature.id == self.SHARK:
                    self.nb_shark += 1
                elif the_creature.id == self.FISH:
                    self.nb_fish += 1

    def remove_dead(self):
        for creature in self.creatures:
            if creature.dead:
                self.creatures.remove(creature)
                if creature.energy < 0:  # to separate the case where a creature is dead because of being
                    # eaten or because loosing all is energy, it's important because if the creature have been eaten
                    # you should change the cell to an empty cell because the predator took the place of the prey
                    self.data[-creature.y][creature.x] = 0

