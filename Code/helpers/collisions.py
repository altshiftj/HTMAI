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


def move_collision(animal, wall, move_dir):
    """
    Function move_collision takes in Animal, Wall, and move direction (backward or forward), then calculates
    whether or not continuing to move constitutes a collision between Wall and Animal
    """

    # wall position and length
    w_x1 = wall.x1
    w_y1 = wall.y1
    w_x2 = wall.x2
    w_y2 = wall.y2
    w_length = wall.length

    # animal position and size
    a_x = animal.x
    a_y = animal.y
    a_radius = animal.size

    # animals next potential moves, forward and backward
    a_x_next_forward = a_x + 0.1 * math.cos(math.radians(animal.head_direction))
    a_y_next_forward = a_y + 0.1 * math.sin(math.radians(animal.head_direction))
    a_x_next_back = a_x - 0.1 * math.cos(math.radians(animal.head_direction))
    a_y_next_back = a_y - 0.1 * math.sin(math.radians(animal.head_direction))

    # a buffer zone around wall end points
    buffer = a_radius

    # Distance from animal to wall start and end points
    dist_2_w1 = dist(a_x,a_y , w_x1,w_y1)
    dist_2_w2 = dist(a_x,a_y , w_x2,w_y2)

    # Distance from animal to wall start point at next timestep
    dist_2_w1_next = dist(a_x_next_forward,a_y_next_forward , w_x1,w_y1)
    dist_2_w2_next = dist(a_x_next_forward,a_y_next_forward , w_x2,w_y2)

    # if animal is at or closer to wall endpoints than its size, and if its next move brings it even closer,
    # a collision is detected. If the next move takes animal further away, no collision is detected.
    if (a_radius >= dist_2_w1 > dist_2_w1_next) or (a_radius >= dist_2_w2 > dist_2_w2_next):
        return True

    # calculate a point that intersects the wall and a vector normal to animal position
    dot = ( ((a_x-w_x1)*(w_x2-w_x1)) + ((a_y-w_y1)*(w_y2-w_y1)) ) / (w_length * w_length)
    x_closest = w_x1 + (dot * (w_x2-w_x1))
    y_closest = w_y1 + (dot * (w_y2-w_y1))

    # distance from this point to wall endpoints
    dot_dist1 = dist(x_closest,y_closest , w_x1,w_y1)
    dot_dist2 = dist(x_closest,y_closest , w_x2,w_y2)

    # If the point of closest distance between animal and wall is outside the endpoints of the wall, 
    # there is no collision
    if not w_length-buffer <= dot_dist1+dot_dist2 <= w_length+buffer:
        return False

    # calculate distance from animal to the nearest wall point
    adist = dist(x_closest,y_closest , a_x,a_y)

    # calculate this distance at next time step
    adist_next_forward = dist(x_closest,y_closest , a_x_next_forward,a_y_next_forward)
    adist_next_back = dist(x_closest, y_closest , a_x_next_back, a_y_next_back)

    # if animal is at or closer to wall than its size, and if its next move brings it even closer,
    # a collision is detected. If the next move takes animal further away, no collision is detected.
    if a_radius >= adist > adist_next_forward and move_dir:
        return True
    elif a_radius >= adist > adist_next_back and not move_dir:
        return True

    return False

def check_collision(animal, box):
    for wall in box.walls:
        collision = move_collision(animal, wall, True)
        if collision:
            return True
    return False