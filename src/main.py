from asyncio.proactor_events import constants
import pygame
from pygame.sprite import collide_mask
from draw_board import draw_board
import sprites
import constants as const

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
)

pygame.init()   # Initialize the pygame module

FPS = 30  # frames per second setting (number of times the screen refreshes per second)
clock = pygame.time.Clock()

# Create a surface, which represents the VIEW component of MVC of (width, height)
# This surface will function as the "root" display
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

# Create and resize surfaces for pieces
red_surf = pygame.image.load('src/images/red_piece.png')
blue_surf = pygame.image.load('src/images/blue_piece.png')
red_surf = pygame.transform.scale(red_surf, (40, 40))
blue_surf = pygame.transform.scale(blue_surf, (40, 40))

class Piece(pygame.sprite.Sprite):
    """ Represent a game piece - each has a color: r(ed) or b(lue) """
    def __init__(self, color):
        # When using the Sprite class, you must call this in the init function
        super(Piece, self).__init__()
        self.color = color
        self.surf = red_surf if self.color == 'r' else blue_surf

class Square:
    """ Represents a square on the board, including its position and width """
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(col*width)
        self.y = int(row*width)
        self.highlighted = False
        self.piece = None

    def draw(self, view):
        if self.highlighted:
            # Draw a filled rectangle before drawing the border so it will appear filled
            pygame.draw.rect(view, const.Color.Gray,
                            (self.x, self.y, const.SQUARE_SIZE, const.SQUARE_SIZE))
        pygame.draw.rect(view, const.Color.Black,
                        (self.x, self.y, const.SQUARE_SIZE, const.SQUARE_SIZE), const.SQUARE_THICKNESS)
        if self.piece is not None:
            surf_to_draw = self.piece.surf
            surf_center = (self.x+5, self.y+5)
            view.blit(surf_to_draw, surf_center)

def create_board():
    """ Creates the board with squares in the appropriate locations - this is the MODEL """
    board = [[None for col in range(const.BOARD_SIZE)] for row in range(const.BOARD_SIZE)]
    for row in range(const.BOARD_SIZE):
        for col in range(const.BOARD_SIZE):
            if row == 0 or row == 8:
                # We want an entire row of squares for the top and bottom rows
                board[row][col] = Square(row, col, const.SQUARE_SIZE-const.SQUARE_THICKNESS)
            else:
                # For other rows, we want only the first and last positions to be squares
                if col == 0 or col == 8:
                    board[row][col] = Square(row, col, const.SQUARE_SIZE-const.SQUARE_THICKNESS)
    return board

def initialize_pieces(board):
    """ Randomly assign two pieces on the board for the human and computer players """
    pass

def die_roll():
    """ Simulates rolling one six-sided die, returning the result (int) """
    pass

def show_possible_moves(board, roll):
    """ Checks the possible moves on the board using the result of the die roll """
    pass

def draw_board(board, screen):
    """ Draws the board for the game, which is a 9x9 grid with a 'hollow' center
        This is the method that converts the MODEL to the VIEW """
    # Create a board surface of the appropriate size based on constant
    view_width = const.BOARD_SIZE*(const.SQUARE_SIZE-const.SQUARE_THICKNESS)+10
    view_height = const.BOARD_SIZE*(const.SQUARE_SIZE-const.SQUARE_THICKNESS)+10
    view = pygame.Surface((view_width, view_height))

    view.fill(const.Color.White)

    # # Set values to use to move the origin as each square is drawn
    # origin_left, origin_top = 0, 0
    # row_min, col_min, row_max, col_max = 0, 0, const.BOARD_SIZE-1, const.BOARD_SIZE-1
    # # This is used to ensure that squares' edges collapse into each other rather than stacking; otherwise, the inner
    # # borders would be thicker than the outer ones
    # space_to_move = const.SQUARE_SIZE-const.SQUARE_THICKNESS
    # for row in range(const.BOARD_SIZE):  # 0-8
    #     origin_left = 0  # Reset after each row
    #     for col in range(const.BOARD_SIZE):  # 0-8
    #         if row == row_min or row == row_max:
    #             pygame.draw.rect(board, const.Color.Black,
    #                              (origin_left, origin_top, const.SQUARE_SIZE, const.SQUARE_SIZE), const.SQUARE_THICKNESS)
    #         else:
    #             if col == col_min or col == col_max:
    #                 pygame.draw.rect(board, const.Color.Black,
    #                                  (origin_left, origin_top, const.SQUARE_SIZE, const.SQUARE_SIZE), const.SQUARE_THICKNESS)
    #         origin_left += space_to_move
    #     origin_top += space_to_move

    # TODO: TEST CODE UNTIL 'END TEST CODE' - REMOVE
    board[0][0].piece = Piece('r')
    board[0][0].highlighted = True
    board[8][8].piece = Piece('b')
    board[8][8].highlighted = True
    # END TEST CODE

    # Draw pieces on board (if they are in a spot)
    for row in board:
        for col in row:
            if col:
                col.draw(view)

    # Calculate the exact center of the board for calling the blit method
    view_center = (
            (const.SCREEN_WIDTH-view.get_width())/2,
            (const.SCREEN_HEIGHT-view.get_height())/2
    )

    screen.blit(view, view_center)

def main():
    """ Set up the game and run the main game loop
    This functions as the CONTROLLER component of MVC """

    # Create a board (MODEL) to be used for storing game data
    board = create_board()

    # Load piece sprites, which will be drawn onto the surface

    # As long as running is True, the game will continue
    running = True

    while running:  # Main game loop
        # Look through new events generated this iteration
        for event in pygame.event.get():
            # Check if the user hit a key
            if event.type == KEYDOWN:
                # If the key pressed was Escape, stop the game loop
                if event.key == K_ESCAPE:
                    running = False
            
            # If the user clicked the window close button, stop the game loop
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 == left click
                    print("click! at", event.pos)
                if event.button == 3:  # 3 == right click
                    print("right click!")

        # Update game objects and data structures (i.e., Model of MVC) here

        # Everything must be drawn from scratch each time the game loop runs.
        # So first fill everything with the background color
        screen.fill(const.Color.White)

        # Reflect the changes to the Model onto the View for the User

        # Draw the board onto the screen
        draw_board(board, screen)

        # The flip method updates the entire screen with every change since it was last called
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()   # If the game loop is exited, quit the game and close the window.

if __name__ == '__main__':
    main()  # Actually run the game.