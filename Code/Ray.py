import pygame

from helpers.collisions import *
from helpers.geometry import *

class Ray:
    """
    Class Ray defines an object with position, orientation, and length. These values are updated based on
    ray caster position and head direction, in conjunction with obstacle positions in the environment
    x - x-position
    y - y-position
    angle = orientation (degrees)
    """
    def __init__(self, x, y, alloc_angle, ego_angle, max_length, color='black'):
        self.x1 = x
        self.y1 = y

        self.alloc_angle = normalize_angle(alloc_angle)
        self.ego_angle = normalize_angle(ego_angle)

        self.length = 1
        self.max_length = max_length

        self.x2 = self.x1 + self.length * math.cos(math.radians(self.alloc_angle))
        self.y2 = self.y1 + self.length * math.sin(math.radians(self.alloc_angle))

        self.color = color
        self.color_num = 0


    def update(self, x, y, alloc_angle, box):
        """Function update takes in an x, y, and angle, and updates the ray to this position and orientation"""
        self.x1 = x
        self.y1 = y
        self.alloc_angle = normalize_angle(alloc_angle)

        ray_collision(self, box)

        return


    def draw(self, display):
        """Function draw defines how a ray is drawn"""
        pygame.draw.line(display, self.color, (self.x1,self.y1) , (self.x2,self.y2), 5)
