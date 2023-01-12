from pygame.locals import *             # import for quit
from opensimplex import OpenSimplex    #
import matplotlib
import csv

matplotlib.use("TkAgg")

from helpers.display_temp_mem import *
from helpers.save_3d_scatters import *
from print_cells_csv import *

plt.ion()

from Box import *
from Animal import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""
#instantiate Box
box = Box(1600,1600)

#instantiate Animal
mouse = Animal(x_pos=400,
               y_pos=800,
               size=20,
               head_direction=0,
               limb_length=40,
               field_of_view=60,
               num_of_rays=10)
learning = True
MOUSE_SPEED = 3
THOUGHT_STEP = 1
track = -1

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

ITERATIONS = 10000
RECORD_ITERATIONS = 1000
START_RECORDING = ITERATIONS - RECORD_ITERATIONS
count = 0

# region Autoturn
# Create an instance of the OpenSimplex noise generator
noise = OpenSimplex(seed=1)

# Generate the directions using OpenSimplex noise
simplex = [i * 0.0075 for i in range(ITERATIONS)]
xdir = [noise.noise2(i, 0) for i in simplex]
ydir = [noise.noise2(0, i) for i in simplex]
# endregion

1

def draw():
    """
    draw function manages all objects to be displayed on the screen
    """
    # black background
    display.fill(('white'))

    # draw Box with internal objects
    box.draw(display)

    # draw Animal, including casted vision rays
    mouse.draw(display)

    # draw image
    screen_box.blit(display, (0, 0))

    # update the display
    pygame.display.update()


# to do while running pygame
while count<ITERATIONS - 1:
    # Animal actions, i.e. look and move.
    keys = pygame.key.get_pressed()

    # Display neural activity
    if keys[pygame.K_c]:
        display_active_cells(mouse.brain.cc1.L23_tm, mouse.brain.cc1.L23_tm_info)

    if keys[pygame.K_v]:
        display_active_freq(mouse.brain.cc1.L23_tm, mouse.brain.cc1.L23_tm_info)

    if keys[pygame.K_f]:
        display_active_cells(mouse.brain.cc1.L4_tm, mouse.brain.cc1.L4_tm_info)

    if keys[pygame.K_g]:
        display_active_freq(mouse.brain.cc1.L4_tm, mouse.brain.cc1.L4_tm_info)

    if keys[pygame.K_t]:
        display_active_cells(mouse.brain.cc1.L6a_tm, mouse.brain.cc1.L6a_tm_info)

    if keys[pygame.K_y]:
        display_active_freq(mouse.brain.cc1.L6a_tm, mouse.brain.cc1.L6a_tm_info)

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

    mouse.move(MOUSE_SPEED, xdir[count], ydir[count], box, 'forward')
    mouse.look(box)

    if count % THOUGHT_STEP==0:
        mouse.think(track, MOUSE_SPEED, THOUGHT_STEP, learning)

    if count == START_RECORDING:
        track *= -1
        learning = False

    count+=1

#save HTM files
mouse.brain.cc1.L6a_tm.saveToFile('locTM', 'BINARY')
mouse.brain.cc1.L6a_sp.saveToFile('locSP', 'BINARY')
mouse.brain.cc1.L4_tm.saveToFile('senTM', 'BINARY')
mouse.brain.cc1.L4_sp.saveToFile('senSP', 'BINARY')
mouse.brain.cc1.L23_tm.saveToFile('objTM', 'BINARY')
mouse.brain.cc1.L23_sp.saveToFile('objSP', 'BINARY')

#create and save neural firing plots
print_cells_csv()
save_3d_scatters()
