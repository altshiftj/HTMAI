import math

import htm
from htm.bindings.sdr import *
from htm.encoders import *
from htm.bindings.algorithms import SpatialPooler
from htm.bindings.algorithms import TemporalMemory
from helpers.encode_helper import *
from helpers.display_SDR import *

from Ray import *


# number of rays in vision array
class Eye:
    """
    Eye Class defines an array of rays cast out in an environment. Rays are cast out in a width range about
    a head direction.

    x - start x-position of rays
    y - starting y-position of rays
    direction - orientation of center ray (degrees)
    vision - array of rays
    field_of_view - width range of ray orientations
    number_of_rays - quantity of rays in vision array
    """

    def __init__(self, x, y, direction, field_of_view, min_vision, max_vision, number_of_rays):
        self.vision = []
        self.field_of_view = field_of_view
        self.number_of_rays = number_of_rays
        self.min_vision = min_vision
        self.max_vision = max_vision
        self.direction = direction

        ang = 0
        del_angle = int(self.field_of_view/(self.number_of_rays))
        start = self.direction - int(self.field_of_view/2)
        while ang*del_angle<=self.field_of_view:
            self.vision.append(Ray(x, y, start+ang*del_angle, int(-self.field_of_view/2+ang/del_angle), max_vision))
            ang+=1

        return


    def see(self, box, x, y, direction):
        """Function see updates position and orientation of rays in vision to input x, y, and direction,
        checks for collisions and updates their endpoints accordingly"""
        i = 0
        for ray in self.vision:
            ray.update(x, y, direction-int(self.field_of_view/2)+(int(self.field_of_view/(self.number_of_rays)))*i, box)
            i += 1

        return


    def draw(self,display):
        """Function draw defines displaying rays in vision"""
        for ray in self.vision:
            ray.draw(display)
