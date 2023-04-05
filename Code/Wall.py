import pygame
from helpers.geometry import *


class Wall:
    """
    Class Wall defines an object with a start point, end point, and color.
    Walls block cast Rays and Animal movement

    :param x1, y1   (int): start position
    :param x2, y2   (int): end position
    :param color    (str): wall color
    """
    def __init__(self, x1,y1, x2,y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.length = dist(x1,y1, x2,y2)
        self.color_num = color

        if color == 1:
            self.color = 'red'
        elif color == 2:
            self.color = 'orange'
        elif color == 3:
            self.color = 'yellow'
        elif color == 4:
            self.color = 'green'
        elif color == 5:
            self.color = 'blue'
        else:
            self.color = 'purple'


    def draw(self, display):
        """Function draw defines how a wall is drawn"""
        pygame.draw.line(display, self.color, (self.x1,self.y1), (self.x2,self.y2), 15)
