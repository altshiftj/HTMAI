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
    """
    Find the intersection point between a ray and a wall (two 2-D line segments), if it exists.

    :param ray      (Ray): The ray to check for intersection with the wall.
    :param wall     (Wall): The wall to check for intersection with the ray.
    :return         tuple of floats or None: The intersection point as a tuple (x, y) if it exists, else None.
    """

    w_x1, w_y1 = wall.x1, wall.y1
    w_x2, w_y2 = wall.x2, wall.y2

    r_x1, r_y1 = ray.x1, ray.y1
    r_x2 = ray.x1 + ray.length * math.cos(math.radians(ray.alloc_angle))
    r_y2 = ray.y1 + ray.length * math.sin(math.radians(ray.alloc_angle))

    # Using line-line intersection formula to get intersection point of ray and wall
    # Where (w_x1, w_y1), (w_x2, w_y2) are the wall pos and (r_x1, r_y1), (r_x2, r_y2) are the ray pos
    denominator = (w_x1 - w_x2) * (r_y1 - r_y2) - (w_y1 - w_y2) * (r_x1 - r_x2)
    if denominator == 0:
        return None
    numerator = (w_x1 - r_x1) * (r_y1 - r_y2) - (w_y1 - r_y1) * (r_x1 - r_x2)
    t = numerator / denominator
    u = -((w_x1 - w_x2) * (w_y1 - r_y1) - (w_y1 - w_y2) * (w_x1 - r_x1)) / denominator

    if 1 > t > 0 and u > 0:
        i_x = w_x1 + t * (w_x2 - w_x1)
        i_y = w_y1 + t * (w_y2 - w_y1)
        return i_x, i_y


def normalize_angle_0_360(angle):
    """
    Normalize an angle to the range [0, 360).
    """
    return angle % 360

def normalize_angle_neg180_180(angle):
    """
    Normalize an angle to the range [-180, 180).
    """
    angle = angle % 360
    if angle >= 180:
        angle -= 360
    return angle