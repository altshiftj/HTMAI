import math

from Code.Animal import *
from Code.Box import *


def main():
    box = Box(2000, 2000)

    mouse = Animal(x_pos=0,
                   y_pos=0,
                   size=10,
                   head_direction=0,
                   limb_length=10,
                   field_of_view=1,
                   num_of_rays=1,
                   color='black')

    MOUSE_SPEED = 0.1

    # loop 100 times
    for i in range(100):
        xdir = math.cos(math.radians(i))
        ydir = math.sin(math.radians(i))

        mouse.move(MOUSE_SPEED, xdir, ydir, box,'forward')
        mouse.left_limb.print()

if __name__ == '__main__':
    main()