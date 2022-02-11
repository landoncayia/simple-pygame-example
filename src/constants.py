from pygame import Color
from pygame import font
from enum import Enum

# Define constants for screen width and height, in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define constants for drawing images in View
SQUARE_SIZE = 50
SQUARE_THICKNESS = 3

# Define constants for board size, width, and height in pixels, as well as the board's origin
BOARD_SIZE = 9
BOARD_WIDTH = BOARD_SIZE*(SQUARE_SIZE-SQUARE_THICKNESS)+10
BOARD_HEIGHT = BOARD_SIZE*(SQUARE_SIZE-SQUARE_THICKNESS)+10
# Calculate the exact center of the board for calling the blit method
BOARD_ORIGIN = (
    (SCREEN_WIDTH-BOARD_WIDTH)/2,
    (SCREEN_HEIGHT-BOARD_HEIGHT)/2
)

# Define Color class to store various useful color values
# This is a great way to do "enums" in Python
class Color:
    Black = (0, 0, 0)
    Gray = (200, 200, 200)
    DarkGray = (50, 50, 50)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Teal = (0, 137, 123)

# Define constants for colors used in game View
BACKGROUND_COLOR = Color.White