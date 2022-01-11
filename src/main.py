import pygame
from pygame.sprite import collide_mask
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
        print(constants.Color.White)
        screen.fill(constants.Color.White)

        # Reflect the changes to the Model onto the View for the User

        # TODO: remove code from here to END TEST when done
        surf = pygame.Surface((50, 50))
        surf.fill(constants.Color.Black)
        rect = surf.get_rect()

        surf_center = (
            (constants.SCREEN_WIDTH-surf.get_width())/2,
            (constants.SCREEN_HEIGHT-surf.get_height())/2
        )
        screen.blit(surf, surf_center)
        # END TEST

        # The flip method updates the entire screen with every change since it was last called
        pygame.display.flip()

    pygame.quit()   # If the game loop is exited, quit the game and close the window.

main()  # Actually run the game.