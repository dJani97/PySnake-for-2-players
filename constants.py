from enum import IntEnum

"""
 _________ Constants file for Snake Game _________ 

"""


"""
Game settings
"""

serial_read_loop_delay = 0.016
fps = 8
block_size = 20
apple_size = 32
apple_count = 1

res_x = 600
res_y = 600


class Dir(IntEnum):
    left = 1
    right = 2
    down = 3
    up = 4


"""
Colors
"""


white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
green = (0, 155, 0)
light_green = (0, 205, 0)  # Hovering
dark_green = (0, 80, 0)
purple = (214, 32, 211)
blue = (0, 0, 255)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
