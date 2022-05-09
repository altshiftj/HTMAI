# import for quit
from pygame.locals import *

# import for display and update
import pygame

# import for exit
import sys

from Box import *
from Animal import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""
#instantiate Box
box = Box(1200,800)
box.add_object(100,100,200,200)
box.add_object(900,600,1100,750)

#instantiate Animal
mouse = Animal(600,400,10,0,270)

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

def draw():
    """
    draw function manages all objects to be displayed on the screen
    """
    # black background
    display.fill((0, 0, 0))

    # draw Box with internal objects
    box.draw(display)

    # draw Animal, including casted vision rays
    mouse.draw(display)

    # draw image
    screen.blit(display, (0, 0))

    # update the display
    pygame.display.update()

# to do while running pygame
while running:

    # Animal actions, i.e. look and move.
    # current inputs, mouse moves forward
    mouse.move(0.01,box,'forward')
    mouse.turn(0.01)
    mouse.look(box)

    # capture events in pygame i.e. exit, keystrokes, etc.
    for event in pygame.event.get():

        # candle exiting the window
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

    # draw all shapes/images
    draw()