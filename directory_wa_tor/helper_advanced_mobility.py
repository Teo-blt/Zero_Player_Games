#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: August 11 11:40:00 2023
# For Wi6labs, all rights reserved
# =============================================================================
"""The Module Has Been Build try zero player games"""
# =============================================================================
# Imports


# ============================================================================
def give_the_best_possible_movement(scan: list):
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    weight_up = 0
    weight_right = 0
    weight_down = 0
    weight_left = 0
    result = []  # défault result, do not move
    for x, y in scan:
        if abs(x) == abs(y):
            if x < 0 and y < 0:  # 1 if close 0.25 if far away
                weight_up += 2 - (abs(x) - 1) * 1.75
                weight_left += 2 - (abs(x) - 1) * 1.75
            elif x < 0 < y:
                weight_up += 2 - (abs(x) - 1) * 1.75
                weight_right += 2 - (abs(x) - 1) * 1.75
            elif x > 0 > y:
                weight_down += 2 - (abs(x) - 1) * 1.75
                weight_left += 2 - (abs(x) - 1) * 1.75
            else:
                weight_down += 2 - (abs(x) - 1) * 1.75
                weight_right += 2 - (abs(x) - 1) * 1.75
        else:
            if x == -2:
                if y == 0:
                    weight_up += 0.75
                else:
                    weight_up += 0.5
            if x == 2:
                if y == 0:
                    weight_down += 0.75
                else:
                    weight_down += 0.5
            if y == -2:
                if x == 0:
                    weight_left += 0.75
                else:
                    weight_left += 0.5
            if y == 2:
                if x == 0:
                    weight_right += 0.75
                else:
                    weight_right += 0.5
    if weight_up == max(weight_up, weight_right, weight_down, weight_left):
        result.append(up)
    if weight_right == max(weight_up, weight_right, weight_down, weight_left):
        result.append(right)
    if weight_down == max(weight_up, weight_right, weight_down, weight_left):
        result.append(down)
    if weight_left == max(weight_up, weight_right, weight_down, weight_left):
        result.append(left)
    return result  # up or right or down or left

"""
distance in step from the center 

4 3 2 3 4
3 1 / 1 3
2 / 0 / 2
3 1 / 1 3
4 3 2 3 4

1 step weight = 2
2 step weight = 0.75
3 step weight = 0.5
4 step weight = 0.25
"""
