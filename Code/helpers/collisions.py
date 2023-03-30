import math

from helpers.geometry import *

"""
Collision helper is a collection of mathematical functions used to calculate collisions between objects
"""
def ray_collision(ray, box):
    """
    Function ray_collision takes in a Ray and Box and calculates shortest collision between a Ray and Walls in Box
    """

    # initial closest point is the max length within box
    closest = math.sqrt(box.width*box.width + box.height*box.height)

    # find all intersections between ray and walls. Set ray length to shortest collision distance
    for wall in box.walls:
        intersect_point = find_intersect(ray, wall)
        if intersect_point is not None:
            ray.length = int(dist(ray.x1, ray.y1, intersect_point[0], intersect_point[1]))
            if (ray.length < closest):
                closest = int(ray.length)
                ray.color = wall.color
                ray.color_num = wall.color_num
    if ray.max_length<closest:
        ray.length = ray.max_length
        ray.color = 'black'
        ray.color_num = 0
    ray.x2 = ray.x1 + ray.length * math.cos(ray.alloc_angle)
    ray.y2 = ray.y1 + ray.length * math.sin(ray.alloc_angle)
    return


def move_collision(animal, wall):
    def next_position(animal, distance_multiplier):
        x_next = animal.x_pos + distance_multiplier * math.cos(math.radians(animal.head_direction))
        y_next = animal.y_pos + distance_multiplier * math.sin(math.radians(animal.head_direction))
        return x_next, y_next

    def is_collision(dist_current, dist_next, a_radius):
        return a_radius >= dist_current > dist_next

    def is_within_wall_buffer(dist1, dist2, w_length, buffer):
        return w_length - buffer <= dist1 + dist2 <= w_length + buffer

    a_x_next_forward, a_y_next_forward = next_position(animal, 0.1)
    buffer = animal.size

    dist_w1_current = dist(animal.x_pos, animal.y_pos, wall.x1, wall.y1)
    dist_w2_current = dist(animal.x_pos, animal.y_pos, wall.x2, wall.y2)
    dist_w1_next = dist(a_x_next_forward, a_y_next_forward, wall.x1, wall.y1)
    dist_w2_next = dist(a_x_next_forward, a_y_next_forward, wall.x2, wall.y2)

    if is_collision(dist_w1_current, dist_w1_next, animal.size) or is_collision(dist_w2_current, dist_w2_next, animal.size):
        return True

    dot = (((animal.x_pos - wall.x1) * (wall.x2 - wall.x1)) + ((animal.y_pos - wall.y1) * (wall.y2 - wall.y1))) / (wall.length ** 2)
    x_closest = wall.x1 + (dot * (wall.x2 - wall.x1))
    y_closest = wall.y1 + (dot * (wall.y2 - wall.y1))

    dot_dist1 = dist(x_closest, y_closest, wall.x1, wall.y1)
    dot_dist2 = dist(x_closest, y_closest, wall.x2, wall.y2)

    if not is_within_wall_buffer(dot_dist1, dot_dist2, wall.length, buffer):
        return False

    adist_current = dist(x_closest, y_closest, animal.x_pos, animal.y_pos)
    adist_next_forward = dist(x_closest, y_closest, a_x_next_forward, a_y_next_forward)

    if is_collision(adist_current, adist_next_forward, animal.size):
        return True

    return False


def check_collision(animal, box):
    for wall in box.walls:
        collision = move_collision(animal, wall)
        if collision:
            return True
    return False
