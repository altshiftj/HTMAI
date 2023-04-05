from Code.CorticalColumn import *
from Code.Ray import *
import time

def main():
    x = 0
    y = 0

    vision = []
    eye_direction = 0
    field_of_view = 40
    number_of_rays = 4
    max_vision = 1200

    ang = 0
    del_angle = int(field_of_view/(number_of_rays))
    start = eye_direction - int(field_of_view/2)
    while ang*del_angle<=field_of_view:
        vision.append(Ray(x, y, start+ang*del_angle, int(-field_of_view/2+ang*del_angle), max_vision))
        ang+=1

    motions = [1,1,1]

    test_cc = CorticalColumn(vision, 128, 4)

    test_cc.initialize(vision, motions)

    # start = time.time()
    # for i in range(1001):
    #     test_cc.process(vision,motions,True)
    # end = time.time()
    #
    # total_time = end-start
    #
    # print(total_time)

    return

if __name__ == '__main__':
    main()