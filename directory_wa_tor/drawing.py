#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: August 9 15:00:00 2023
# For Zero_player_game, all rights reserved
# =============================================================================
"""The Module Has Been Build try zero player games"""
# =============================================================================
# Imports
import matplotlib.pyplot as plt


# ============================================================================

class Application:
    def __init__(self, y_values1, y_values2):
        self.y_values1 = y_values1
        self.y_values2 = y_values2
        self.x_values = []

        # Sample data
        x_values = [i for i in range(len(self.y_values1))]

        # Create a line graph for the first line
        plt.plot(x_values, self.y_values1, label='Number of fish')

        # Create a line graph for the second line
        plt.plot(x_values, self.y_values2, label='Number of shark')

        # Add labels, title, and legend
        plt.xlabel('Time')
        plt.ylabel('Quantity')
        plt.title('Number of fish and shark through time')
        plt.legend()

        # Display the graph
        plt.show()
