from asyncio.proactor_events import constants
from re import X
from shutil import move
import pygame
from pygame.sprite import collide_mask
from draw_board import draw_board
import sprites
import constants as const
import random

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

# Create and resize surfaces for die sides
one_surf = pygame.image.load('src/images/die-one.png')
two_surf = pygame.image.load('src/images/die-two.png')
three_surf = pygame.image.load('src/images/die-three.png')
four_surf = pygame.image.load('src/images/die-four.png')
five_surf = pygame.image.load('src/images/die-five.png')
six_surf = pygame.image.load('src/images/die-six.png')
one_surf = pygame.transform.scale(one_surf, (40, 40))
two_surf = pygame.transform.scale(two_surf, (40, 40))
three_surf = pygame.transform.scale(three_surf, (40, 40))
four_surf = pygame.transform.scale(four_surf, (40, 40))
five_surf = pygame.transform.scale(five_surf, (40, 40))
six_surf = pygame.transform.scale(six_surf, (40, 40))

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
        self.selected = False
        self.capturable = False
        self.piece = None

    def draw(self, view):
        if self.highlighted:
            # Draw a filled rectangle before drawing the border so it will appear filled
            pygame.draw.rect(view, const.Color.LightGray,
                            (self.x, self.y, const.SQUARE_SIZE, const.SQUARE_SIZE))
        if self.selected:
            # Draw over the previous rectangle with medium gray because it is a square
            # of a selected piece
            pygame.draw.rect(view, const.Color.MediumGray,
                            (self.x, self.y, const.SQUARE_SIZE, const.SQUARE_SIZE))
        if self.capturable:
            # Do the same as highlighted, except make it tinted red to indicate capturability
            pygame.draw.rect(view, const.Color.CaptureRed,
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

def reset_board_attributes(board, h, s, c):
    """ Resets whichever board attributes are specified """
    for row in range(const.BOARD_SIZE):
        for col in range(const.BOARD_SIZE):
            if row == 0 or row == 8:
                if h:
                    board[row][col].highlighted = False
                if s:
                    board[row][col].selected = False
                if c:
                    board[row][col].capturable = False
            else:
                if col == 0 or col == 8:
                    if h:
                        board[row][col].highlighted = False
                    if s:
                        board[row][col].selected = False
                    if c:
                        board[row][col].capturable = False

def move_left(row, col):
    """ Helper function for find_square; moves counter-clockwise one square """
    if row == 0:
        if col == 0:
            # Upper-left corner -> move down a square
            row += 1
        else:
            # First row -> move left a square
            col -= 1
    elif col == 0:
        if row == 8:
            # Lower-left corner -> move right a square
            col += 1
        else:
            # First col -> move down a square
            row += 1
    elif row == 8:
        if col == 8:
            # Lower-right corner -> move up a square
            row -= 1
        else:
            # Last row -> move right a square
            col += 1
    elif col == 8:
        if row == 0:
            # Upper-right corner -> move left a square
            col -= 1
        else:
            # Last col -> move up a square
            row -= 1
    return row, col
    
def move_right(row, col):
    """ Helper function for find_square; moves clockwise one square """
    if row == 0:
        if col == 8:
            # Upper-right corner -> move down a square
            row += 1
        else:
            # First row -> move right a square
            col += 1
    elif col == 8:
        if row == 8:
            # Lower-right corner -> move left a square
            col -= 1
        else:
            # Last col -> move down a square
            row += 1
    elif row == 8:
        if col == 0:
            # Lower-left corner -> move up a square
            row -= 1
        else:
            # Last row -> move left a square
            col -= 1
    elif col == 0:
        if row == 0:
            # Upper-left corner -> move right a square
            col += 1
        else:
            # First col -> move up a square
            row -= 1
    return row, col

def find_square(start, count, direction):
    """ Determine which square is 'count' squares away from 'start' in
    'direction' ('l' for left/counter-clockwise or 'r' for right/clockwise) """
    row = start[0]
    col = start[1]
    
    for _ in range(count):
        if direction == 'l':
            row, col = move_left(row, col)
        else:
            row, col = move_right(row, col)
    return row, col

def initialize_pieces(board):
    """ Randomly assign two pieces on the board for the human and computer players """
    # Pick four random locations, without replacement; first two are human
    # player's piece locations, second two are computer player's piece locations
    sample = random.sample(range(32), 4)
    for n in range(4):
        start_pos = [0, 0]
        # Starting from the top-left square, move n squares clockwise to find piece's initial location
        piece_row, piece_col = find_square(start_pos, sample[n], 'r')
        # First two positions for red, second two for blue
        if n in [0, 1]:
            board[piece_row][piece_col].piece = Piece('r')
        else:
            board[piece_row][piece_col].piece = Piece('b')


def die_roll():
    """ Simulates rolling one six-sided die, returning the result (int) """
    return random.randint(1, 6)

def find_possible_moves(board, roll, player):
    """ Checks the possible moves on the board using the result of the die roll """
    for row in board:
        for square in row:
            if square and square.piece:
                # If we land on a square, and the square contains a piece
                if square.piece.color == 'b' and player == 'p':
                    # Get the square that is 'roll' squares counter-clockwise
                    row_left, col_left = find_square((square.row, square.col), roll, 'l')
                    # Get the square that is 'roll' squares clockwise
                    row_right, col_right = find_square((square.row, square.col), roll, 'r')
                    # We don't want the square to be an eligible move if a piece of the same color is on it
                    if board[row_left][col_left].piece and board[row_left][col_left].piece.color == 'r':
                        board[row_left][col_left].capturable = True
                    elif not board[row_left][col_left].piece:
                        board[row_left][col_left].highlighted = True
                    if board[row_right][col_right].piece and board[row_right][col_right].piece.color == 'r':
                        board[row_right][col_right].capturable = True
                    elif not board[row_right][col_right].piece:
                        board[row_right][col_right].highlighted = True

def coords_to_square(pos_x, pos_y):
    """ Converts pixel coordinates from the user's pointer location to a square """
    for col in range(9):
        for row in range(9):
            x = const.BOARD_ORIGIN[0]+(col*47)  # have to add board's x origin to get the right spot
            y = const.BOARD_ORIGIN[1]+(row*47)  # have to add board's y origin to get the right spot
            if x < pos_x < x+47 and y < pos_y < y+47:
                return row, col

def draw_view(board, screen, roll=None):
    """ Draws the view for the game, which includes:
        The board, the current game state and the die-rolling mechanism
        This is the method that converts the MODEL to the VIEW """

    # ===== BOARD =====
    # Create a board surface of the appropriate size based on constant
    view_board = pygame.Surface((const.BOARD_WIDTH, const.BOARD_HEIGHT))
    view_board.fill(const.Color.White)
    # Draw pieces on board (if they are in a spot)
    for row in board:
        for col in row:
            if col:
                col.draw(view_board)
    screen.blit(view_board, const.BOARD_ORIGIN)

    # ===== DIE ROLLING =====
    view_die = pygame.Surface((140, 300))
    view_die.fill(const.Color.White)
    pygame.draw.rect(view_die, const.Color.Teal, (0, 0, 140, 300), 5)
    pygame.draw.rect(view_die, const.Color.DarkGray, (26, 50, 85, 45), 3)
    # Define font for text
    font = pygame.font.SysFont(None, 36)
    roll_txt = font.render('Roll', True, const.Color.Red)
    view_die.blit(roll_txt, (45, 60))
    # If there is a die roll, display the correct die
    if roll:
        if roll == 1:
            view_die.blit(one_surf, (45, 160))
        if roll == 2:
            view_die.blit(two_surf, (45, 160))
        if roll == 3:
            view_die.blit(three_surf, (45, 160))
        if roll == 4:
            view_die.blit(four_surf, (45, 160))
        if roll == 5:
            view_die.blit(five_surf, (45, 160))
        if roll == 6:
            view_die.blit(six_surf, (45, 160))
    screen.blit(view_die, (23, 150))

def main():
    """ Set up the game and run the main game loop
    This functions as the CONTROLLER component of MVC """

    # Create a board (MODEL) to be used for storing game data
    board = create_board()

    # Set initial piece locations on board for start of game
    initialize_pieces(board)

    # As long as running is True, the game will continue
    running = True

    # Variable to hold the current state of the game
    #   proll indicates that it is the player's turn to roll the die
    #   croll indicates that it is the computer's turn to roll the die
    #   pmove indicates that the player may move without capturing a piece
    #   cmove indicates that the computer may move without capturing a piece
    #   pcptr indicates that the player may capture a computer piece
    #   ccptr indicates that the computer may capture a player piece
    #   gmovr indicates that the game is over; someone has won
    # Human player always gets the first move
    state = 'proll'
    active_player = 'p'  # p or c

    # Variable to hold the current die roll result
    roll = None

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

            if state == 'proll':
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # 1 == left click
                        pos_x, pos_y = event.pos
                        if 50 < pos_x < 135 and 200 < pos_y < 245:
                            roll = die_roll()
                            state = 'pmove'

            elif state == 'pmove':
                find_possible_moves(board, roll, active_player)
                # Keep track of which piece the player has selected to move
                selected_square = [None]
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos_x, pos_y = event.pos
                        print(type(pos_x), type(pos_y))
                        row, col = coords_to_square(pos_x, pos_y)
                        if board[row][col].piece and board[row][col].piece.color == 'b':
                            # Blue (player) selected one of his/her pieces
                            # First, clear any other selections ONLY
                            reset_board_attributes(board, False, True, False)
                            selected_row, selected_col = row, col
                            board[selected_row][selected_col].selected = True
                        elif selected_square:
                            # Blue (player) has a square selected
                            if not board[row][col].piece:
                                # Blue (player) moved to an empty square
                                board[row][col].piece = Piece('b')
                                board[selected_row][selected_col].piece = None
                                # Reset all board attributes; player's turn is over
                                reset_board_attributes(board, True, True, True)
                                state = 'croll'
                            else:
                                # Blue (player) has clicked on a square with a piece
                                if board[row][col].piece.color == 'r' and board[row][col].capturable:
                                    # Blue (player) captures a red piece
                                    board[row][col].piece = Piece('b')
                                    board[selected_row][selected_col].piece = None
                                    # Reset all board attributes; player's turn is over
                                    reset_board_attributes(board, True, True, True)
                                    state = 'croll'
                            
            # if event.type == MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         pos_x, pos_y = event.pos
            #         row, col = coords_to_square(pos_x, pos_y)
            #     if event.button == 3:  # 3 == right click
            #         print("right click!")

        # Update game objects and data structures (i.e., Model of MVC) here

        # Everything must be drawn from scratch each time the game loop runs.
        # So first fill everything with the background color
        screen.fill(const.Color.White)

        # Reflect the changes to the Model onto the View for the User
        # Draw the board onto the screen
        draw_view(board, screen, roll)

        # The flip method updates the entire screen with every change since it was last called
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()   # If the game loop is exited, quit the game and close the window.

if __name__ == '__main__':
    main()  # Actually run the game.