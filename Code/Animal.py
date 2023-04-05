from Brain import *
from Eye import *
from helpers.collisions import *


class Animal:
    """
    A class representing an animal with vision and movement capabilities.

    :param x_pos            (int): The x-coordinate of the animal's position.
    :param y_pos            (int): The y-coordinate of the animal's position.
    :param size             (int): The size of the animal.
    :param head_direction   (float): The direction the animal's head is facing.
    :param field_of_view    (float): The field of view of the animal's vision.
    :param num_of_rays      (int): The number of rays used in the animal's vision.
    :param speed            (int): The speed at which the animal moves.
    :param thought_freq     (int): The frequency of the animal's thoughts.
    :param cc_width         (int): The width of the animal's cortical column.
    :param cc_layer_depth   (int): The depth of layers in the animal's cortical column.
    :param color            (str, optional): The color of the animal. Defaults to 'black'.
    """
    def __init__(self, x_pos, y_pos, size, head_direction, field_of_view, num_of_rays, speed, thought_freq, cc_width, cc_layer_depth, color='black'):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.distance_travelled = 0
        self.speed = speed
        self.angular_velocity = 0

        self.size = size

        self.head_direction = head_direction
        self.field_of_view = field_of_view

        self.eye = Eye(x_pos, y_pos, head_direction, field_of_view, size, 1600, num_of_rays)

        self.brain = Brain(vision = self.eye.vision, learning = True, record_activity = False, cc_width = cc_width, cc_layer_depth = cc_layer_depth)
        self.thought_freq = thought_freq

        self.color = color


    def look(self, box):
        """
        Updates the animal's vision by having its eye see the given environment.

        :param: box     (Box): The environment that the animal is in.
        """
        self.eye.see(box, self.x_pos, self.y_pos, self.head_direction)


    def think(self):
        """
        Animal thinks and updates its state based on its current state.
        """
        # If the animal has not thought yet, initialize its brain
        if self.brain.thought_count == 0:
            self.brain.initialize(self.eye.vision, self.distance_travelled, self.speed, self.angular_velocity)
        else:
            # train the HTM network based on the current state
            self.brain.think(self.x_pos, self.y_pos, self.head_direction, self.eye.vision, self.distance_travelled, self.speed, self.angular_velocity)

        # if distance travelled is greater than 4 times the speed, reset it. They cyclic nature of the distance travelled
        # can be likened to the cyclic nature of limb movement.
        if self.distance_travelled>4*self.speed:
            self.distance_travelled = 0

        self.angular_velocity = 0
        return


    def move(self, box):
        """
        Moves the animal in its current direction if there is no collision.

        :param box      (Box): The environment that the animal is in.
        """
        if not check_collision(self, box):
            self.distance_travelled += self.speed
            self.x_pos += self.speed * math.cos(math.radians(self.head_direction))
            self.y_pos += self.speed * math.sin(math.radians(self.head_direction))

        return


    def turn(self, xdir, ydir):
        """
        Turn an object based on the input x and y directions.

        :param xdir     (float): X direction.
        :param ydir     (float): Y direction.
        """
        # Calculate the angle between the positive X-axis and the vector (xdir, ydir) in degrees
        target_angle = normalize_angle_0_360(math.degrees(math.atan2(ydir, xdir)))

        current_angle = self.head_direction

        # Calculate the angle difference between the target angle and the current angle
        angle_difference = normalize_angle_neg180_180(target_angle - current_angle)

        self.angular_velocity += round(angle_difference)
        self.head_direction = round(target_angle)

        return


    def draw(self, display):
        """
        Draws the animal and its vision on the given display.
        """
        self.eye.draw(display)
        pygame.draw.circle(display, self.color, (self.x_pos, self.y_pos), self.size, 5)
        pygame.draw.circle(display, 'white', (self.x_pos, self.y_pos), self.size - 5)