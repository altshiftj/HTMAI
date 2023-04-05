import math

from helpers.geometry import *

"""
This script contains functions for detecting collisions between rays and walls, as well as between animals and walls.

Functions
- ray_collision: Determines the shortest collision distance between a Ray object and the walls in a Box object,
                 updating the Ray object with the closest intersection point and corresponding wall color.
- move_collision: Checks for collisions between an Animal object and a Wall object, returning True if a collision is found,
                  and False otherwise.
- check_collision: Checks for collisions between an Animal object and the walls contained in a Box object, returning True
                   if a collision is found, and False otherwise.
"""

def ray_collision(ray, box):
    """
    Calculates the shortest collision distance between a Ray object and the walls contained in a Box object.

    :param ray      (Ray): The Ray object to calculate collisions for.
    :param box      (Box): The Box object containing the walls to check for collisions against.
    :return Ray:    The updated Ray object, including the closest intersection point with a wall and the corresponding wall color.
    """

    # Initialize closest to the maximum possible distance within the box
    closest = math.sqrt(box.width ** 2 + box.height ** 2)

    # Iterate over all walls in the box, checking for intersections with the ray
    for wall in box.walls:
        intersect_point = find_intersect(ray, wall)
        if intersect_point is not None:
            # If an intersection is found, update the ray length and closest intersection point
            ray.length = int(dist(ray.x1, ray.y1, intersect_point[0], intersect_point[1]))
            # If this collision is closer than previous collisions, it is now the closest. Update the color of the ray
            if ray.length < closest:
                closest = int(ray.length)
                ray.color = wall.color
                ray.color_num = wall.color_num

    # If no intersections were found, set the ray length to its maximum length
    if ray.max_length < closest:
        ray.length = ray.max_length
        ray.color = 'black'
        ray.color_num = 0

    # Update the end point of the ray based on the new length and angle
    ray.x2 = ray.x1 + ray.length * math.cos(math.radians(ray.alloc_angle))
    ray.y2 = ray.y1 + ray.length * math.sin(math.radians(ray.alloc_angle))

    # Return the updated Ray object
    return ray


def move_collision(animal, wall):
    """
    Checks for collisions between an Animal object and a Wall object.

    :param animal   (Animal): The Animal object to check for collisions against the wall.
    :param wall     (Wall): The Wall object to check for collisions against the animal.
    :return bool:   True if a collision is found, False otherwise.
    """

    # Function to calculate the next position of the animal
    def next_position(animal, distance_multiplier):
        x_next = animal.x_pos + distance_multiplier * math.cos(math.radians(animal.head_direction))
        y_next = animal.y_pos + distance_multiplier * math.sin(math.radians(animal.head_direction))
        return x_next, y_next

    # Function to check if there is a collision between the animal and the wall
    def is_collision(dist_current, dist_next, a_radius):
        return a_radius >= dist_current > dist_next

    # Function to check if the distance between the animal and the closest point of the wall is within the wall buffer
    def is_within_wall_buffer(dist1, dist2, w_length, buffer):
        return w_length - buffer <= dist1 + dist2 <= w_length + buffer

    # Calculate the next position of the animal by moving it forward by 0.1 distance multiplier
    a_x_next_forward, a_y_next_forward = next_position(animal, 0.1)
    buffer = 0

    # Calculate the distance between the animal and the two endpoints of the wall (current and next position)
    dist_w1_current = dist(animal.x_pos, animal.y_pos, wall.x1, wall.y1)
    dist_w2_current = dist(animal.x_pos, animal.y_pos, wall.x2, wall.y2)
    dist_w1_next = dist(a_x_next_forward, a_y_next_forward, wall.x1, wall.y1)
    dist_w2_next = dist(a_x_next_forward, a_y_next_forward, wall.x2, wall.y2)

    # Check if there is a collision between the animal and the wall at the current and next positions
    if is_collision(dist_w1_current, dist_w1_next, animal.size) or is_collision(dist_w2_current, dist_w2_next,
                                                                                animal.size):
        return True

    # Calculate the distance between the animal and the closest point of the wall
    dot = (((animal.x_pos - wall.x1) * (wall.x2 - wall.x1)) + ((animal.y_pos - wall.y1) * (wall.y2 - wall.y1))) / (
                wall.length ** 2)
    x_closest = wall.x1 + (dot * (wall.x2 - wall.x1))
    y_closest = wall.y1 + (dot * (wall.y2 - wall.y1))

    # Calculate the distances between the closest point of the wall and the two endpoints of the wall
    dot_dist1 = dist(x_closest, y_closest, wall.x1, wall.y1)
    dot_dist2 = dist(x_closest, y_closest, wall.x2, wall.y2)

    # Check if the distance between the animal and the closest point of the wall is within the wall buffer
    if not is_within_wall_buffer(dot_dist1, dot_dist2, wall.length, buffer):
        return False

    # Calculate the distance between the animal and the closest point of the wall at the current and next positions
    adist_current = dist(x_closest, y_closest, animal.x_pos, animal.y_pos)
    adist_next_forward = dist(x_closest, y_closest, a_x_next_forward, a_y_next_forward)

    # Check if there is a collision between the animal and the wall at the closest point at the current and next positions
    if is_collision(adist_current, adist_next_forward, animal.size):
        return True

    return False

def check_collision(animal, box):
    """
    Checks for collisions between an Animal object and the walls contained in a Box object.

    :param animal   (Animal): The Animal object to check for collisions against walls.
    :param box      (Box): The Box object containing the walls to check for collisions against.
    :return bool:   True if a collision is found, False otherwise.
    """

    # Iterate over all walls in the box, checking for collisions with the animal
    for wall in box.walls:
        collision = move_collision(animal, wall)
        if collision:
            # If a collision is found, return True to indicate that a collision occurred
            return True

    # If no collisions are found, return False
    return False