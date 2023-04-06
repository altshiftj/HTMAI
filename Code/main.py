from pygame.locals import *
from perlin_noise import PerlinNoise
from pathlib import Path
import matplotlib
import pygame.font

matplotlib.use("TkAgg")

from helpers.display_temp_mem import *
from helpers.neural_activity_read_write import sort_cell_activity, save_3d_scatters

plt.ion()

from Box import *
from Animal import *

"""
Purpose of main is to manage the relationship between class Box and Animal, as well as implement pygame display
"""

# define the length of training and how long to record neural activity
ITERATIONS = 4000
RECORD_ITERATIONS = 100; assert RECORD_ITERATIONS < ITERATIONS
BEGIN_RECORDING = ITERATIONS - RECORD_ITERATIONS
count = 0

#instantiate Box
box = Box(width = 1024, height = 1024)

#instantiate Animal
mouse = Animal(x_pos = 200,
               y_pos = 400,
               size = 20,
               head_direction = 0,
               field_of_view = 60,
               num_of_rays = 11,
               speed = 5,
               thought_freq = 10,
               cc_width = 64,
               cc_layer_depth = 32,)

# region Autoturn: Generate a set of random directions for the animal to travel in
# NOTE: Changing noise scale will affect the sporadic nature of the turns. A higher noise scale will result in more
#       sporadic turns.
noisex = PerlinNoise(octaves=2)
noisey = PerlinNoise(octaves=3)
NOISE_SCALE = 0.0025
perlin = [i * NOISE_SCALE for i in range(ITERATIONS)]
xdir = [noisex(i) for i in perlin]
ydir = [noisey(i) for i in perlin]
# endregion

#initialize pygame environment
pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen_box = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

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

    font = pygame.font.Font(None, 36)
    text = font.render(f"Count: {count}", 1, (0, 0, 0))
    display.blit(text, (10, 10))

    # draw image
    screen_box.blit(display, (0, 0))

    # update the display
    pygame.display.update()


# to do while running pygame
while count<ITERATIONS - 1:
    # Capture keystroke events
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

    #capture events in pygame i.e. exit, keystrokes, etc.
    for event in pygame.event.get():

        # handle exiting the window
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

    # update the mouse position and direction
    mouse.turn(xdir[count], ydir[count])
    mouse.move(box)

    # cast vision rays at new position
    mouse.look(box)

    # train the HTM network every thought_freq iteration
    if count % mouse.thought_freq==0:
        mouse.think()

    # stop learning and start recording neural activity
    if count == BEGIN_RECORDING:
        mouse.brain.stop_learning()
        mouse.brain.start_recording()


    # draw all shapes/images
    draw()

    count+=1

#save HTM files
layer_path = Path(__file__).parent.parent / 'Output/Saved_Networks'
layer_path.mkdir(parents=True, exist_ok=True)
mouse.brain.cc1.L6a_tm.saveToFile(f'{layer_path}/locTM', 'BINARY')
mouse.brain.cc1.L6a_sp.saveToFile(f'{layer_path}/locSP', 'BINARY')
mouse.brain.cc1.L4_tm.saveToFile(f'{layer_path}/senTM', 'BINARY')
mouse.brain.cc1.L4_sp.saveToFile(f'{layer_path}/senSP', 'BINARY')
mouse.brain.cc1.L23_tm.saveToFile(f'{layer_path}/objTM', 'BINARY')
mouse.brain.cc1.L23_sp.saveToFile(f'{layer_path}/objSP', 'BINARY')

#create and save neural firing plots
sort_cell_activity(mouse.brain.cc1.column_width, mouse.brain.cc1.layer_depth)
save_3d_scatters(box.height, box.width, mouse.brain.cc1.column_width, mouse.brain.cc1.layer_depth)
