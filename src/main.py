import pygame
from pygame.sprite import collide_mask
from draw_board import draw_board
import sprites
import constants

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Piece:
    """ Represent a game piece - each has a color: r(ed) or b(lue) """
    def __init__(self, color):
        self.color = color
        self.image = 'piece_red.png' if self.color == 'r' else 'piece_blue.png'

def initialize_pieces(board):
    """ Randomly assign two pieces on the board for the human and computer players """
    pass

def die_roll():
    """ Simulates rolling one six-sided die, returning the result (int) """
    pass

def show_possible_moves(board, roll):
    """ Checks the possible moves on the board using the result of the die roll """
    pass

def draw_board(screen):
    """ Draws the board for the game, which is a 9x9 grid with a 'hollow' center
        This is the method that converts the MODEL to the VIEW """
    # Create a board surface of the appropriate size based on constant
    board = pygame.Surface((constants.BOARD_SIZE*50+10, constants.BOARD_SIZE*50+10))
    board.fill(constants.Color.White)

    # Set values to use to move the origin as each square is drawn
    origin_left, origin_top = 0, 0
    row_min, col_min, row_max, col_max = 0, 0, constants.BOARD_SIZE-1, constants.BOARD_SIZE-1
    # This is used to ensure that squares' edges collapse into each other rather than stacking; otherwise, the inner
    # borders would be thicker than the outer ones
    space_to_move = constants.SQUARE_SIZE-constants.SQUARE_THICKNESS
    for row in range(constants.BOARD_SIZE):  # 0-8
        origin_left = 0  # Reset after each row
        for col in range(constants.BOARD_SIZE):  # 0-8
            if row == row_min or row == row_max:
                pygame.draw.rect(board, constants.Color.Black,
                                 (origin_left, origin_top, constants.SQUARE_SIZE, constants.SQUARE_SIZE), 3)
            else:
                if col == col_min or col == col_max:
                    pygame.draw.rect(board, constants.Color.Black,
                                     (origin_left, origin_top, constants.SQUARE_SIZE, constants.SQUARE_SIZE), 3)
            origin_left += space_to_move
        origin_top += space_to_move

    # Calculate the exact center of the board for calling the blit method
    board_center = (
            (constants.SCREEN_WIDTH-board.get_width())/2,
            (constants.SCREEN_HEIGHT-board.get_height())/2
    )

    screen.blit(board, board_center)

def main():
    """ Set up the game and run the main game loop
    This functions as the Controller component of MVC """
    pygame.init()   # Initialize the pygame module

    # Create a surface, which represents the View component of MVC of (width, height)
    # This surface will function as the "root" display
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    # Load piece sprites, which will be drawn onto the surface

    # As long as running is True, the game will continue
    running = True

    # Main game loop
    while running:
        # Look through new events generated this iteration
        for event in pygame.event.get():
            # Check if the user hit a key
            if event.type == KEYDOWN:
                # If the key pressed was Escape, stop the game loop
                if event.key == K_ESCAPE:
                    running = False
            
            # If the user clicked the window close button, stop the game loop
            elif event.type == QUIT:
                running = False

        # Update game objects and data structures (i.e., Model of MVC) here

        # Everything must be drawn from scratch each time the game loop runs.
        # So first fill everything with the background color
        screen.fill(constants.Color.White)

        # Reflect the changes to the Model onto the View for the User

        # Draw the board onto the screen
        draw_board(screen)

        # The flip method updates the entire screen with every change since it was last called
        pygame.display.flip()

    pygame.quit()   # If the game loop is exited, quit the game and close the window.

if __name__ == '__main__':
    main()  # Actually run the game.