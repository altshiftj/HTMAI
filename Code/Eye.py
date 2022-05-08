from htm.bindings.sdr import SDR

from Ray import *
from Code.helpers.collisions import *

number_of_rays = 30
class Eye:
    def __init__(self, x, y, direction, field_of_view):
        self.vision = []
        self.field_of_view = field_of_view
        for i in range(direction - int(field_of_view / 2), direction + int(field_of_view / 2),int(field_of_view/number_of_rays)):
            self.vision.append(Ray(x, y, i))

    def see(self, box, x, y, direction):
        i = 0
        for ray in self.vision:
            ray.update(x, y, direction-int(self.field_of_view/2)+(int(self.field_of_view/number_of_rays))*i)
            ray_collision(ray, box)
            i += 1

    def encode(self):
        pass

    def draw(self,display):
        for ray in self.vision:
            ray.draw(display)
