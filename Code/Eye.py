from htm.bindings.sdr import SDR

from Ray import *


# number of rays in vision array
number_of_rays = 30
class Eye:
    """
    Eye Class defines an array of rays cast out in an environment. Rays are cast out in a width range about
    a head direction. Length and orientation of each ray are encoded into an SDR to be sent to Brain for
    Spatial Pooling

    x - start x-position of rays
    y - starting y-position of rays
    direction - orientation of center ray (degrees)
    vision - array of rays
    field_of_view - width range of ray orientations
    number_of_rays - quantity of rays in vision array
    """

    def __init__(self, x, y, direction, field_of_view):
        self.vision = []
        self.field_of_view = field_of_view

        for a in range(direction - int(field_of_view / 2), direction + int(field_of_view / 2),
                       int(field_of_view/number_of_rays)):
            self.vision.append(Ray(x, y, a))


    def see(self, box, x, y, direction):
        """Function see updates position and orientation of rays in vision to input x, y, and direction,
        checks for collisions and updates their endpoints accordingly"""
        i = 0
        for ray in self.vision:
            ray.update(x, y, direction-int(self.field_of_view/2)+(int(self.field_of_view/number_of_rays))*i, box)
            i += 1


    def encode(self):
        """Function encode encodes the length and orientation of each ray in vision into SDRs"""
        pass


    def draw(self,display):
        """Function draw defines displaying rays in vision"""
        for ray in self.vision:
            ray.draw(display)
