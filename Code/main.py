# import for quit
from pygame.locals import *

# import for display and update
import pygame

# import for exit
import sys

from Box import *
from Animal import *

box = Box(1200,800)
box.add_object(100,100,200,200)
box.add_object(900,600,1100,750)

mouse = Animal(600,400,10,0,270)

pygame.init()
WINDOW_SIZE = (box.width,box.height)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
running = True

def draw():
    display.fill((0, 0, 0))

    box.draw(display)
    mouse.draw(display)

    screen.blit(display, (0, 0))

    pygame.display.update()

while running:
    mouse.move(0.01,box,'forward')
    mouse.turn(0.01)
    mouse.look(box)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

    draw()