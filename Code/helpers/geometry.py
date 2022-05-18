import math

"""
Geometry helper is a place to define basic geometric operations that are often used.
"""
def dist(x1,y1 , x2,y2):
    """Function dist calculates the distance between two 2-D points"""
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt((dx * dx) + (dy * dy))


def find_intersect(ray, wall):
    """Function find_intersect find the intersection between a ray and a wall (two 2-D line segments), if it exists"""
    w_x1 = wall.x1
    w_y1 = wall.y1
    w_x2 = wall.x2
    w_y2 = wall.y2

    r_x1 = ray.x1
    r_y1 = ray.y1
    r_x2 = ray.x1 + ray.length * math.cos(ray.angle)
    r_y2 = ray.y1 + ray.length * math.sin(ray.angle)

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
    
    def find_move_intersection(animal, wall, move_step):
        w_x1 = wall.x1
        w_y1 = wall.y1
        w_x2 = wall.x2
        w_y2 = wall.y2

        a_x1 = animal.x1
        r_y1 = animal.y1
        r_x2 = animal.x1 + (move_step) * math.cos(math.radians(animal.head_direction))
        r_y2 = animal.y1 + (move_step) * math.sin(math.radians(animal.head_direction))

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


def dot (x1,y1 , x2,y2):
    pass