from pygame.locals import *
import pygame
import sys
import random
import math

def ray_collision(ray, walls):
    closest = 100000
    for wall in walls:
        intersect_point = find_intersect(ray, wall)
        if intersect_point is not None:
            ray.length = dist(ray.x1, ray.y1, intersect_point[0], intersect_point[1])
            if (ray.length < closest):
                closest = ray.length
    ray.length = closest
    ray.update_end_point()

def move_collision(ray, wall, key):
    w_x1 = wall.x1
    w_y1 = wall.y1
    w_x2 = wall.x2
    w_y2 = wall.y2
    w_length = wall.length

    a_x = ray.x1
    a_y = ray.y1
    a_radius = ray.size

    a_x_next_forward = a_x + 0.1 * math.cos(ray.angle)
    a_y_next_forward = a_y + 0.1 * math.sin(ray.angle)
    a_x_next_back = a_x - 0.1 * math.cos(ray.angle)
    a_y_next_back = a_y - 0.1 * math.sin(ray.angle)

    buffer = a_radius

    # Distance to wall start point
    dist_2_w1 = dist(a_x,a_y , w_x1,w_y1)

    # Distance to wall end point
    dist_2_w2 = dist(a_x,a_y, w_x2,w_y2)

    # Distance to wall start point at next timestep
    dist_2_w1_next = dist(a_x_next_forward,a_y_next_forward , w_x1,w_y1)
    dist_2_w2_next = dist(a_x_next_forward, a_y_next_forward, w_x2, w_y2)

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
    cdist_next_back = dist(x_closest, y_closest, a_x_next_back, a_y_next_back)

    if a_radius >= cdist > cdist_next_forward and key[pygame.K_UP]:
        return True
    elif a_radius >= cdist > cdist_next_back and key[pygame.K_DOWN]:
        return True

    return False

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


pygame.init()

# -----Options-----
WINDOW_SIZE = (1200, 800)  # Width x Height in pixels
NUM_RAYS = 3  # Must be between 1 and 360
SOLID_RAYS = False  # Can be somewhat glitchy. For best results, set NUM_RAYS to 360
NUM_WALLS = 5  # The amount of randomly generated walls
# ------------------

screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)

mx, my = (600, 400)
running = True
rays = []
walls = []
particles = []
head_direction = 0
field_of_view = 120
del_angle = 0
del_pos = 0
hit = False

class Ray:

    def __init__(self, x, y, angle, color='white'):
        self.x1 = x
        self.y1 = y

        self.angle = math.radians(angle)
        self.length = 1

        self.x2 = self.x1+self.length*math.cos(self.angle)
        self.y2 = self.y1+self.length*math.sin(self.angle)

        self.color = color

        self.size = 10

    def update(self, del_mx, del_my, del_ang):
        self.x1 += del_mx * math.cos(math.radians(head_direction))
        self.y1 += del_my * math.sin(math.radians(head_direction))
        self.angle += math.radians(del_ang)
        self.x2 = self.x1 + self.length * math.cos(self.angle)
        self.y2 = self.y1 + self.length * math.sin(self.angle)

    def update_end_point(self):
        self.x2 = self.x1 + self.length * math.cos(self.angle)
        self.y2 = self.y1 + self.length * math.sin(self.angle)

    def draw(self):
        pygame.draw.line(display, self.color, (self.x1,self.y1) , (self.x2,self.y2))

class Wall:
    def __init__(self, x1, y1, x2, y2, color='white'):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.length = dist(x1, y1, x2, y2)

    def draw(self):
        pygame.draw.line(display, self.color, (self.x1, self.y1), (self.x2, self.y2), 3)


for i in range(head_direction-int(field_of_view/2), head_direction+int(field_of_view/2),4):
    rays.append(Ray(mx, my, i))


def move_collision(ray, wall, key):
    w_x1 = wall.x1
    w_y1 = wall.y1
    w_x2 = wall.x2
    w_y2 = wall.y2
    w_length = wall.length

    a_x = ray.x1
    a_y = ray.y1
    a_radius = ray.size

    a_x_next_forward = a_x + 0.1 * math.cos(ray.angle)
    a_y_next_forward = a_y + 0.1 * math.sin(ray.angle)
    a_x_next_back = a_x - 0.1 * math.cos(ray.angle)
    a_y_next_back = a_y - 0.1 * math.sin(ray.angle)

    buffer = a_radius

    # Distance to wall start point
    dist_2_w1 = dist(a_x,a_y , w_x1,w_y1)

    # Distance to wall end point
    dist_2_w2 = dist(a_x,a_y, w_x2,w_y2)

    # Distance to wall start point at next timestep
    dist_2_w1_next = dist(a_x_next_forward,a_y_next_forward , w_x1,w_y1)
    dist_2_w2_next = dist(a_x_next_forward, a_y_next_forward, w_x2, w_y2)

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
    cdist_next_back = dist(x_closest, y_closest, a_x_next_back, a_y_next_back)

    if a_radius >= cdist > cdist_next_forward and key[pygame.K_UP]:
        return True
    elif a_radius >= cdist > cdist_next_back and key[pygame.K_DOWN]:
        return True

    return False


def drawRays(rays, walls):
    for ray in rays:
        ray_collision(ray,walls)
        ray.draw()

    pygame.draw.circle(display, rays[0].color, (rays[0].x1, rays[0].y1), rays[0].size)


def generateWalls():
    walls.clear()

    walls.append(Wall(0, 0, WINDOW_SIZE[0], 0))
    walls.append(Wall(0, 0, 0, WINDOW_SIZE[1]))
    walls.append(Wall(WINDOW_SIZE[0], 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
    walls.append(Wall(0, WINDOW_SIZE[1], WINDOW_SIZE[0], WINDOW_SIZE[1]))

    for i in range(NUM_WALLS):
        start_x = random.randint(0, WINDOW_SIZE[0])
        start_y = random.randint(0, WINDOW_SIZE[1])
        end_x = random.randint(0, WINDOW_SIZE[0])
        end_y = random.randint(0, WINDOW_SIZE[1])
        walls.append(Wall(start_x, start_y, end_x, end_y))


def draw():
    display.fill((0, 0, 0))

    for wall in walls:
        wall.draw()

    for particle in particles:
        particle.draw()

    drawRays([ray for ray in rays], [wall for wall in walls])

    screen.blit(display, (0, 0))

    pygame.display.update()


generateWalls()
while running:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        del_angle = 1
        for ray in rays:
            ray.update(0, 0, del_angle)
        head_direction += del_angle

    if keys[pygame.K_LEFT]:
        del_angle = -1
        for ray in rays:
            ray.update(0, 0, del_angle)
        head_direction += del_angle

    if keys[pygame.K_UP]:
        for wall in walls:
            hit = move_collision(rays[int(len(rays)/2)], wall , keys)
            if hit:
                break
        if not hit:
            for ray in rays:
                del_pos = 1
                ray.update(del_pos, del_pos, 0)

    if keys[pygame.K_DOWN]:
        for wall in walls:
            hit = move_collision(rays[int(len(rays)/2)], wall, keys)
            if hit:
                break
        if not hit:
            for ray in rays:
                del_pos = -1
                ray.update(del_pos, del_pos, 0)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()


        if event.type == KEYDOWN:
            # Re-randomize walls on Space
            if event.key == pygame.K_SPACE:
                generateWalls()



    # for ray in rays:
    #     ray.update(mx, my, math.radians(del_angle))

    draw()

