import pygame
import constants

def draw_board(screen):
    """ Creates a board for the game, which is a 9x9 hollow grid """
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