
from pygame.locals import *             # import for quit
import pygame                           # import for display and update
import sys                              # import for exit
from perlin_noise import PerlinNoise    #
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


from Box import *
from Animal import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""
#instantiate Box
box = Box(1200,800)
box.add_object(100,75,1100,100)
box.add_object(150,175,550,200)
box.add_object(650,175,1050,200)

box.add_object(100,400,200,500)
box.add_object(300,600,500,700)
box.add_object(900,300,1150,475)
box.add_object(575,375,725,450)

#instantiate Animal
mouse = Animal(300,400,10,0,270)

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

# region Autoturn
# noise = PerlinNoise()
count = 0
# perlin = [i*0.001 for i in range(50000)]
# turn = [2*noise(i) for i in perlin]
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




mouse.look(box)
mouse.think()

x_val = [i for i in range(1, mouse.brain.tm_info.dimensions[0] + 1)]
y_val = mouse.brain.tm_info.activationFrequency.activationFrequency

plt.ion()
figure = plt.figure()
ax = figure.add_subplot(111)
line, = ax.plot(x_val,y_val)

# to do while running pygame
while running:
    # Animal actions, i.e. look and move.
    # current inputs, mouse moves forward

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        mouse.turn(.1)

    if keys[pygame.K_LEFT]:
        mouse.turn(-.1)

    if keys[pygame.K_UP]:
        mouse.move(.5,box,'forward')


    # capture events in pygame i.e. exit, keystrokes, etc.
    for event in pygame.event.get():

        # handle exiting the window
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

    # draw all shapes/images

    mouse.look(box)
    draw()

    mouse.think()

    if count % 100 == 0:
        update_y = mouse.brain.tm_info.activationFrequency.activationFrequency
        line.set_ydata(update_y)
        figure.canvas.draw()
        figure.canvas.flush_events()

    # mouse.turn(turn[count])
    # mouse.move(0.1,box,'forward')

    count+=1



