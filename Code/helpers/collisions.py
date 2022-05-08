from Code.helpers.geometry import *


def ray_collision(ray, box):
    closest = math.sqrt(box.width*box.width + box.height*box.height)
    for wall in box.walls:
        intersect_point = find_intersect(ray, wall)
        if intersect_point is not None:
            ray.length = dist(ray.x1, ray.y1, intersect_point[0], intersect_point[1])
            if (ray.length < closest):
                closest = ray.length
    ray.length = closest
    ray.update_end_point()

def move_collision(animal, wall, move_dir):
    w_x1 = wall.x1
    w_y1 = wall.y1
    w_x2 = wall.x2
    w_y2 = wall.y2
    w_length = wall.length

    a_x = animal.x
    a_y = animal.y
    a_radius = animal.size

    a_x_next_forward = a_x + 0.1 * math.cos(animal.head_direction)
    a_y_next_forward = a_y + 0.1 * math.sin(animal.head_direction)
    a_x_next_back = a_x - 0.1 * math.cos(animal.head_direction)
    a_y_next_back = a_y - 0.1 * math.sin(animal.head_direction)

    buffer = a_radius

    # Distance to wall start and end points
    dist_2_w1 = dist(a_x,a_y , w_x1,w_y1)
    dist_2_w2 = dist(a_x,a_y , w_x2,w_y2)

    # Distance to wall start point at next timestep
    dist_2_w1_next = dist(a_x_next_forward,a_y_next_forward , w_x1,w_y1)
    dist_2_w2_next = dist(a_x_next_forward,a_y_next_forward , w_x2,w_y2)

    if (a_radius >= dist_2_w1 > dist_2_w1_next) or (a_radius >= dist_2_w2 > dist_2_w2_next):
        return True

    dot = ( ((a_x-w_x1)*(w_x2-w_x1)) + ((a_y-w_y1)*(w_y2-w_y1)) ) / (w_length * w_length)

    x_closest = w_x1 + (dot * (w_x2-w_x1))
    y_closest = w_y1 + (dot * (w_y2-w_y1))

    dot_dist1 = dist(x_closest,y_closest , w_x1,w_y1)
    dot_dist2 = dist(x_closest,y_closest , w_x2,w_y2)

    if not w_length-buffer <= dot_dist1+dot_dist2 <= w_length+buffer:
        return False

    cdist = dist(x_closest,y_closest , a_x,a_y)
    cdist_next_forward = dist(x_closest,y_closest , a_x_next_forward,a_y_next_forward)
    cdist_next_back = dist(x_closest, y_closest , a_x_next_back, a_y_next_back)

    if a_radius >= cdist > cdist_next_forward and move_dir:
        return True
    elif a_radius >= cdist > cdist_next_back and not move_dir:
        return True

    return False

