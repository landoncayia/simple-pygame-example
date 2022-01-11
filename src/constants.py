from pygame import Color
from enum import Enum

# Define constants for screen width and height, in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define constants for drawing images in View
SQUARE_SIZE = 50
SQUARE_THICKNESS = 3

# Define Color class to store various useful color values
# This is a great way to do "enums" in Python
class Color:
    Black = (0, 0, 0)
    Gray = (127, 127, 127)
    DarkGray = (50, 50, 50)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)

# Define constants for colors used in game View
BACKGROUND_COLOR = Color.White

# Define constants related to game logic/rules
BOARD_SIZE = 9