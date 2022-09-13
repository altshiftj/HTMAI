import numpy as np
from pygame.locals import *             # import for quit
import pygame                           # import for display and update
import sys                              # import for exit
from perlin_noise import PerlinNoise    #
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

from helpers.display_temp_mem import *
plt.ion()

from Box import *
from Animal import *
from Example import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""


#instantiate Box
box = Box(1600,1600)
#box.add_object(100,75,1100,100)
#box.add_object(150,175,550,200)
# box.add_object(650,175,1050,200)
#
# box.add_object(100,400,200,500)
# box.add_object(300,600,500,700)
# box.add_object(900,300,1150,475)
# box.add_object(575,375,725,450)

#instantiate Animal
mouse = Animal(300,200,10,0,270,15)
learning = True
mouse_speed = 3
thought_step = 10
track = -1

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

iterations = 1250000
record_iterations = 50000
record_start = iterations - record_iterations
count = 0

# region Autoturn
noisex = PerlinNoise(octaves=2)
noisey = PerlinNoise(octaves=3)
perlin = [i*0.001 for i in range(iterations)]
xdir = [noisex(i) for i in perlin]
ydir = [noisey(i) for i in perlin]
# endregion

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
while count<iterations - 1:
    # Animal actions, i.e. look and move.
    # current inputs, mouse moves forward

    keys = pygame.key.get_pressed()

    #region Keyboard Move

    if keys[pygame.K_RIGHT]:
        mouse.turn(.5)

    if keys[pygame.K_LEFT]:
        mouse.turn(-.5)

    if keys[pygame.K_UP]:
        mouse.move(1,box,'forward')

    # endregion

    if keys[pygame.K_c]:
        display_active_cells(mouse.brain.cc1.L23_object_tm, mouse.brain.cc1.L23_tm_info)

    if keys[pygame.K_v]:
        display_active_freq(mouse.brain.cc1.L23_object_tm, mouse.brain.cc1.L23_tm_info)

    if keys[pygame.K_f]:
        display_active_cells(mouse.brain.cc1.L4_sensory_tm, mouse.brain.cc1.L4_tm_info)

    if keys[pygame.K_g]:
        display_active_freq(mouse.brain.cc1.L4_sensory_tm, mouse.brain.cc1.L4_tm_info)

    if keys[pygame.K_t]:
        display_active_cells(mouse.brain.cc1.L6a_location_tm, mouse.brain.cc1.L6a_tm_info)

    if keys[pygame.K_y]:
        display_active_freq(mouse.brain.cc1.L6a_location_tm, mouse.brain.cc1.L6a_tm_info)

    if keys[pygame.K_r]:
        track *= -1

    #capture events in pygame i.e. exit, keystrokes, etc.
    for event in pygame.event.get():

        # handle exiting the window
        if event.type == QUIT:
            sys.exit()
            pygame.quit()



    # draw all shapes/images
    draw()

    mouse.look(box)
    mouse.turn(xdir[count], ydir[count])
    mouse.move(mouse_speed, box, 'forward')

    if count%thought_step==0:
        mouse.think(track, mouse_speed, thought_step, learning)

    if count == record_start:
        track *= -1
        learning = False

    count+=1

mouse.brain.cc1.L6a_location_tm.saveToFile('locTM', 'BINARY')
mouse.brain.cc1.L6a_location_sp.saveToFile('locSP', 'BINARY')
mouse.brain.cc1.L4_sensory_tm.saveToFile('senTM', 'BINARY')
mouse.brain.cc1.L4_sensory_sp.saveToFile('senSP', 'BINARY')
mouse.brain.cc1.L23_object_tm.saveToFile('objTM', 'BINARY')
mouse.brain.cc1.L23_object_sp.saveToFile('objSP', 'BINARY')
