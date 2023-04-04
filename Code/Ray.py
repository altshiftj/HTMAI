import pygame

from helpers.collisions import *
from helpers.geometry import *

class Ray:
    """
    A Ray object representing a line segment with position, orientation, and length.

    The ray's position and orientation are updated based on the ray caster's position,
    head direction, and obstacle positions in the environment.

    :param x                (int): The x-coordinate of the starting point of the ray.
    :param y                (int): The y-coordinate of the starting point of the ray.
    :param alloc_angle      (int): The angle allocated to the ray in degrees, relative to the positive x-axis.
    :param ego_angle        (int): The orientation of the ray caster's head in degrees.
    :param max_length       (int): The maximum length of the ray.
    :param color            (str, optional): The color of the ray, represented as a string (default is 'black').
    """
    def __init__(self, x, y, alloc_angle, ego_angle, max_length, color='black'):
        self.x1 = x
        self.y1 = y

        self.alloc_angle = normalize_angle_0_360(alloc_angle)
        self.ego_angle = normalize_angle_0_360(ego_angle)

        self.length = 1
        self.max_length = max_length

        self.x2 = self.x1 + self.length * math.cos(math.radians(self.alloc_angle))
        self.y2 = self.y1 + self.length * math.sin(math.radians(self.alloc_angle))

        self.color = color
        self.color_num = 0


    def update(self, x, y, alloc_angle, box):
        """
        Updates the position and orientation of the ray to the given coordinates and angle.

        :param x            (int): The x-coordinate of the ray's new position.
        :param y            (int): The y-coordinate of the ray's new position.
        :param alloc_angle  (int): The new allocentric angle in degrees of the ray's orientation.
        :param box          (Box): The Box object representing the environment.
        """

        # Update the ray's position and orientation
        self.x1 = x
        self.y1 = y
        self.alloc_angle = normalize_angle_0_360(alloc_angle)

        # Check for collisions with walls in the environment and updates the end point of the ray
        ray_collision(self, box)


    def draw(self, display):
        """Function draw defines how a ray is drawn"""
        pygame.draw.line(display, self.color, (self.x1,self.y1) , (self.x2,self.y2), 5)
