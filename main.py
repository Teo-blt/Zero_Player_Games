#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 20 10:00:00 2023
# For Wi6labs, all rights reserved
# =============================================================================
"""The Module Has Been Build to try zero player games"""
# =============================================================================
# Imports
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import directory_game_of_life.game_of_life
import directory_langton_ant.langton_ant
import directory_brian_brain.brian_brain


# ============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self.title("Zero player games")
        self.color = "#E76145"
        self.current_table = StringVar()
        # Create value lists
        self.combo_list = ["Game of life", "Langton's ant", "Brian's brain", "Wireworld", "Forest fire", "Highlife"]

        # Create widgets
        self.main_window()

    def main_window(self):
        """
        main_window create the HMI window
        """
        finder_frame = ttk.LabelFrame(self, text="Menu")
        finder_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        finder_frame_label = ttk.Label(finder_frame, text="Select the wanted game:")
        finder_frame_label.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        def on_combobox_change(event):
            """
            on_combobox_change Function called when clik by the user create the HMI window
            """
            self.destroy()
            match self.current_table.get():
                case "Game of life":
                    directory_game_of_life.game_of_life.Application().mainloop()
                case "Langton's ant":
                    directory_langton_ant.langton_ant.Application().mainloop()
                case "Brian's brain":
                    directory_brian_brain.brian_brain.Application().mainloop()
                case _:
                    showerror("Error", "Game unknown")

        game_select_combobox = ttk.Combobox(finder_frame, values=self.combo_list, textvariable=self.current_table)
        game_select_combobox.current(0)
        game_select_combobox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        game_select_combobox.bind("<<ComboboxSelected>>", on_combobox_change)

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")


if __name__ == "__main__":
    # execute only if run as a script
    Application().mainloop()
