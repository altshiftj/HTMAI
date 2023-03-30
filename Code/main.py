from pygame.locals import *
from perlin_noise import PerlinNoise
import matplotlib

matplotlib.use("TkAgg")

from helpers.display_temp_mem import *
from helpers.neural_activity_visualization import save_3d_scatters
from Code.print_cells_csv import *

plt.ion()

from Box import *
from Animal import *

"""
Purpose of main is to create and manage the relationship between class Box and Animal, as well as implement pygame display
"""

ITERATIONS = 1000
RECORD_ITERATIONS = 50
START_RECORDING = ITERATIONS - RECORD_ITERATIONS
COUNT = 0

#instantiate Box
box = Box(1600,1600)

#instantiate Animal
mouse = Animal(x_pos = 400,
               y_pos = 800,
               size = 20,
               head_direction = 0,
               field_of_view = 60,
               num_of_rays = 10,
               speed = 5,
               thought_freq = 10,)

#instantiate pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

# region Autoturn
noisex = PerlinNoise(octaves=2)
noisey = PerlinNoise(octaves=3)
perlin = [i * 0.001 for i in range(ITERATIONS)]
xdir = [noisex(i) for i in perlin]
ydir = [noisey(i) for i in perlin]
# endregion


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
while COUNT<ITERATIONS - 1:
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

    mouse.turn(xdir[COUNT], ydir[COUNT])
    mouse.move(box)
    mouse.look(box)

    if COUNT % mouse.thought_freq==0:
        mouse.think()

    if COUNT == START_RECORDING:
        mouse.brain.stop_learning()
        mouse.brain.start_recording()

    COUNT+=1

# save HTM files
mouse.brain.cc1.L6a_tm.saveToFile('locTM', 'BINARY')
mouse.brain.cc1.L6a_sp.saveToFile('locSP', 'BINARY')
mouse.brain.cc1.L4_tm.saveToFile('senTM', 'BINARY')
mouse.brain.cc1.L4_sp.saveToFile('senSP', 'BINARY')
mouse.brain.cc1.L23_tm.saveToFile('objTM', 'BINARY')
mouse.brain.cc1.L23_sp.saveToFile('objSP', 'BINARY')

# create and save neural firing plots
print_cells_csv(mouse.brain.cc1.column_width, mouse.brain.cc1.layer_depth)
save_3d_scatters()
