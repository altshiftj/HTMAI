import numpy as np
from pygame.locals import *             # import for quit
import pygame                           # import for display and update
import csv
import sys                              # import for exit
from perlin_noise import PerlinNoise    #
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

from helpers.display_temp_mem import *
plt.ion()

from Box import *
from Animal import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""
#instantiate Box
box = Box(800,600)
# box.add_object(100,75,1100,100)
# box.add_object(150,175,550,200)
# box.add_object(650,175,1050,200)
#
# box.add_object(100,400,200,500)
# box.add_object(300,600,500,700)
# box.add_object(900,300,1150,475)
# box.add_object(575,375,725,450)

#instantiate Animal
mouse = Animal(300,200,10,0,270)
track = False

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

f = open('cell_fire.csv', 'w', newline='')
header = ['thought count', 'cell', 'column', 'x', 'y']
writer = csv.writer(f)
writer.writerow(header)

# region Autoturn
noisex = PerlinNoise()
noisey = PerlinNoise()
count = 0
perlin = [i*0.003 for i in range(75000)]
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

    mouse.brain.draw_most_active_cell(display)

    # draw image
    screen_box.blit(display, (0, 0))

    # update the display
    pygame.display.update()

# to do while running pygame
while count<74999:
    # Animal actions, i.e. look and move.
    # current inputs, mouse moves forward

    keys = pygame.key.get_pressed()
    #region Keyboard Move (commented)

    if keys[pygame.K_RIGHT]:
        mouse.turn(.5)

    if keys[pygame.K_LEFT]:
        mouse.turn(-.5)

    if keys[pygame.K_UP]:
        mouse.move(1,box,'forward')

    # endregion

    if keys[pygame.K_c]:
        display_active_cells(mouse)

    if keys[pygame.K_f]:
        display_active_freq(mouse)

    if keys[pygame.K_SPACE]:
        mouse.brain.cell_fire_location.clear()
        mouse.brain.find_most_active_neuron(mouse.brain.L6a_location_tm_info)
        track = True


    #capture events in pygame i.e. exit, keystrokes, etc.
    for event in pygame.event.get():

        # handle exiting the window
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

    # draw all shapes/images

    mouse.look(box)

    draw()

    mouse.turn(xdir[count], ydir[count])
    mouse.move(2,box,'forward')

    #if count%1 == 0:
    mouse.think()

    if track:
        mouse.brain.track_most_active_neuron(mouse, mouse.brain.L6a_location_tm)

    if 73900<count<74900 and count%4==0:
        cells_active = mouse.brain.L6a_location_tm.getActiveCells().sparse
        column_number_prev=-1
        for i in range(len(cells_active)):
            cell_number = cells_active[i]
            column_number = mouse.brain.L6a_location_tm.columnForCell(cell_number)
            if column_number == column_number_prev:
                continue
            column_number_prev = mouse.brain.L6a_location_tm.columnForCell(cell_number)
            x = int(mouse.x)
            y = int(mouse.y)

            data = [count, column_number, x, y]
            writer.writerow(data)
    count+=1

mouse.brain.L6atoL4_interlayer_sp.saveToFile('locISP', 'BINARY')
mouse.brain.L6a_location_tm.saveToFile('locTM', 'BINARY')
mouse.brain.L6a_location_sp.saveToFile('locTM', 'BINARY')
mouse.brain.L4toL6a_interlayer_sp.saveToFile('senISP', 'BINARY')
mouse.brain.L4_sensory_tm.saveToFile('senTM', 'BINARY')
mouse.brain.L4_sensory_sp.saveToFile('senSP', 'BINARY')





