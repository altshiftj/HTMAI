import math

import htm
from htm.bindings.sdr import *
from htm.encoders import *
from htm.bindings.algorithms import SpatialPooler
from htm.bindings.algorithms import TemporalMemory
from helpers.encode_helper import *

from Ray import *


# number of rays in vision array
class Eye:
    """
    Eye Class defines an array of rays cast out in an environment. Rays are cast out in a width range about
    a head direction.

    :param: x_pos           (int): start x-position of rays
    :param: y_pos           (int): starting y-position of rays
    :param: direction       (int): orientation of center ray (degrees)
    :param: vision          (list): array of rays
    :param: field_of_view   (int): width range of ray orientations
    :param: number_of_rays  (int): quantity of rays in vision array
    """
    def __init__(self, x_pos, y_pos, direction, field_of_view, min_vision, max_vision, number_of_rays):
        self.vision = []
        self.field_of_view = field_of_view
        self.number_of_rays = number_of_rays
        self.min_vision = min_vision
        self.max_vision = max_vision

        # initialize the eye's vision (an array of rays)
        start_angle = direction - self.field_of_view / 2
        delta_angle = self.field_of_view / (self.number_of_rays -1)
        for i in range(self.number_of_rays):
            alloc_angle = start_angle + i * delta_angle
            ego_angle = -self.field_of_view / 2 + i * delta_angle
            self.vision.append(Ray(x_pos, y_pos, alloc_angle, ego_angle, max_vision))


    def see(self, box, x_pos, y_pos, direction):
        """
        Updates position and orientation of rays in vision to input x, y, and direction.

        :param box          (Box): Box object representing the environment.
        :param x_pos        (int): x-coordinate of the animal's current position.
        :param y_pos        (int): y-coordinate of the animal's current position.
        :param direction    (int): Current direction of the animal's head in degrees.
        """
        i = 0
        for ray in self.vision:
            ray.update(x_pos, y_pos, direction - self.field_of_view / 2 + self.field_of_view / (self.number_of_rays -1) * i, box)
            i += 1

        return


    def draw(self,display):
        """Function draw defines displaying rays in vision"""
        for ray in self.vision:
            ray.draw(display)
