import pygame

from helpers.collisions import *

class Ray:
    """
    Class Ray defines an object with position, orientation, and length. These values are updated based on
    ray caster position and head direction, in conjunction with obstacle positions in the environment
    x - x-position
    y - y-position
    angle = orientation (degrees)
    """
    def __init__(self, x, y, angle, max_length, color='white'):
        self.x1 = x
        self.y1 = y
        self.degree_angle = angle
        if angle>=360:
            self.degree_angle-=360
        if angle<0:
            self.degree_angle+=360
        self.angle = math.radians(self.degree_angle)
        self.length = 1
        self.max_length = max_length
        self.x2 = self.x1 + self.length * math.cos(self.angle)
        self.y2 = self.y1 + self.length * math.sin(self.angle)
        self.color = color


    def update(self, x, y, angle, box):
        """Function update takes in an x, y, and angle, and updates the ray to this position and orientation"""
        self.x1 = x
        self.y1 = y
        self.degree_angle=angle
        if angle>=360:
            self.degree_angle-=360
        if angle<0:
            self.degree_angle+=360
        self.angle = math.radians(angle)

        ray_collision(self, box)

        return




    def draw(self, display):
        """Function draw defines how a ray is drawn"""
        pygame.draw.line(display, self.color, (self.x1,self.y1) , (self.x2,self.y2))
