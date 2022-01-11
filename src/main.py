import pygame as pg  # Using 'as' enables one to reference pygame as 'pg' rather than 'pygame'

def main():
    """ Set up the game and run the main game loop
    This functions as the Controller component of MVC """
    pg.init()                   # Initialize the pygame module
    width, height = 640, 480    # The width and height of the game window

    # Create a surface, which represents the View component of MVC of (width, height), and its window.
    main_surface = pg.display.set_mode((width, height))

    # Set up some data to describe a small rectangle and its color.
    small_rect = (300, 200, 150, 90)
    some_color = (255, 0, 0)        # R G B

    # Main game loop
    while True:
        ev = pg.event.poll()        # Look for any event
        if ev.type == pg.QUIT:      # Window close button clicked?
            break                   # Leave game loop and end game

        # Update game objects and data structures here

        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        main_surface.fill((0, 200, 255))

        # Overpaint a smaller rectangle on the main surface
        main_surface.fill(some_color, small_rect)

        # Now the surface is ready, tell pygame to display it!
        pg.display.flip()

    pg.quit()   # If the game loop is exited, quit the game and close the window.

main()          # Actually run the game.