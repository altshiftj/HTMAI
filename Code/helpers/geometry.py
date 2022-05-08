import math


def dist(x1,y1 , x2,y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt((dx * dx) + (dy * dy))

def find_intersect(ray, wall):
    w_x1 = wall.x1
    w_y1 = wall.y1
    w_x2 = wall.x2
    w_y2 = wall.y2

    r_x1 = ray.x1
    r_y1 = ray.y1
    r_x2 = ray.x2
    r_y2 = ray.y2

    # Using line-line intersection formula to get intersection point of ray and wall
    # Where (w_x1, w_y1), (w_x2, w_y2) are the wall pos and (r_x1, r_y1), (r_x2, r_y2) are the ray pos
    denominator = (w_x1 - w_x2) * (r_y1 - r_y2) - (w_y1 - w_y2) * (r_x1 - r_x2)
    numerator = (w_x1 - r_x1) * (r_y1 - r_y2) - (w_y1 - r_y1) * (r_x1 - r_x2)
    if denominator == 0:
        return None

    t = numerator / denominator
    u = -((w_x1 - w_x2) * (w_y1 - r_y1) - (w_y1 - w_y2) * (w_x1 - r_x1)) / denominator

    if 1 > t > 0 and u > 0:
        i_x = w_x1 + t * (w_x2 - w_x1)
        i_y = w_y1 + t * (w_y2 - w_y1)
        intersect_point = [i_x, i_y]
        return intersect_point