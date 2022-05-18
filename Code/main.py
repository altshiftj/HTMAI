
from pygame.locals import *             # import for quit
import pygame                           # import for display and update
import sys                              # import for exit
from perlin_noise import PerlinNoise    #
import matplotlib.pyplot as plt


from Box import *
from Animal import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""
#instantiate Box
box = Box(800,600)
box.add_object(400,100,500,200)
box.add_object(100,400,200,500)

#instantiate Animal
mouse = Animal(400,300,10,0,270)

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

noise = PerlinNoise()
count = 0
perlin = [i*0.001 for i in range(50000)]
turn = [2*noise(i) for i in perlin]

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
    screen_box.blit(display, (0, 0))

    # update the display
    pygame.display.update()

# to do while running pygame
while running:
    # Animal actions, i.e. look and move.
    # current inputs, mouse moves forward

    # capture events in pygame i.e. exit, keystrokes, etc.
    for event in pygame.event.get():

        # candle exiting the window
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

    # draw all shapes/images

    mouse.look(box)
    draw()

    mouse.think()

    # plt.plot(perlin,turn)
    # plt.show()
    mouse.turn(turn[count])
    mouse.move(0.1,box,'forward')
    count+=1



