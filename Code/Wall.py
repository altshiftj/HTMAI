import pygame
from helpers.geometry import *


class Wall:
    """
    Class Wall defines an object with a start point, end point, and color.
    Walls block cast Rays and Animal movement
    x1, y1 - start position
    x2, y2 - end position
    color - wall color
    """
    def __init__(self, x1,y1, x2,y2, color='white'):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.length = dist(x1,y1, x2,y2)


    def draw(self, display):
        """Function draw defines how a wall is drawn"""
        pygame.draw.line(display, self.color, (self.x1,self.y1), (self.x2,self.y2), 3)
