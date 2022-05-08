import math
import pygame
from Code.helpers.geometry import *


class Wall:
    def __init__(self, x1,y1, x2,y2, color='white'):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.length = dist(x1,y1, x2,y2)

    def draw(self, display):
        pygame.draw.line(display, self.color, (self.x1,self.y1), (self.x2,self.y2), 3)
