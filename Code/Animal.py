from Brain import *
from Eye import *
from helpers.collisions import *


class Animal:
    """
    Animal class defines an object which can move and see in a given environment. Class Animal "sees" with an Eye object
    which casts rays in an environment and encodes their distance and orientation into an SDR. Animal then interprets
    this encoding using Class Brain, which inplements Spatial Pooling to learn patterns of movement and sensation, using
    the learned patterns to decide on future movements.

    x - animal x-position
    y - animal y-position
    size - Animal size, that is drawn radius. Also important in collision calculations
    head_direction - direction of movement and center of Animal vision (degrees)
    field_of_view - angular width of Animal view
    """
    def __init__(self, x, y, size, head_direction, field_of_view, num_of_rays, color='black'):
        self.x = x
        self.y = y
        self.l1_distance = 0
        self.linear_speed = 0
        self.angular_velocity = 0

        self.size = size

        self.head_direction = head_direction
        self.field_of_view = field_of_view

        self.eye = Eye(x, y, head_direction, field_of_view, size, 1200, num_of_rays)
        self.brain = Brain(self.eye.vision)

        self.color = color


    def look(self, box):
        """Function look takes in an environment and looks at it using Eye at Animal x and y in head_direction"""
        self.eye.see(box, self.x, self.y, self.head_direction)


    def think(self, track, move_speed, thought_step, learning):
        """Function think passes encoded Eye SDR to Brain for Spatial Pooling and Temporal Memory functions"""
        if self.brain.thought_count == 0:
            self.brain.initialize(self.eye.vision, self.l1_distance, self.linear_speed, self.angular_velocity)

        self.brain.think(self.eye.vision, self.l1_distance, self.linear_speed, self.angular_velocity, learning)

        if track == 1:
            self.record()

        if self.l1_distance>5*move_speed*thought_step:
            self.l1_distance = 0

        self.angular_velocity = 0
        return

    def record(self):
        write_activecell_to_csv(self.brain.cc1.L23_tm,
                                'L23_active',
                                self.brain.thought_count,
                                int(self.x),
                                int(self.y),
                                int(self.head_direction),
                                '-', '-')

        write_activecell_to_csv(self.brain.cc1.L4_tm,
                                'L4_active',
                                self.brain.thought_count,
                                int(self.x),
                                int(self.y),
                                int(self.head_direction),
                                '-', '-')

        write_activecell_to_csv(self.brain.cc1.L6a_tm,
                                'L6a_active',
                                self.brain.thought_count,
                                int(self.x),
                                int(self.y),
                                int(self.head_direction),
                                self.linear_speed,
                                self.angular_velocity)


    def move(self, step_size_move, box, direction):
        """Function move takes in a step size (speed), environment, and forward or backward direction
        to define movement. Animal moves within the environment checking for collisions as it goes"""

        if not check_collision(self, box):
            self.l1_distance += step_size_move
            self.x += step_size_move * math.cos(math.radians(self.head_direction))
            self.y += step_size_move * math.sin(math.radians(self.head_direction))

        return


    def turn(self, xdir, ydir):
        """
        Turn an object based on the input x and y directions.
        Args:
            xdir (float): X direction.
            ydir (float): Y direction.
        """
        # Calculate the angle between the positive X-axis and the vector (xdir, ydir) in degrees
        target_angle = math.degrees(math.atan2(ydir, xdir))
        target_angle = normalize_angle(target_angle)

        current_angle = self.head_direction
        angle_difference = normalize_angle(target_angle - current_angle)

        if angle_difference > 180:
            angle_difference -= 360

        self.angular_velocity += round(angle_difference)

        self.head_direction = round(target_angle)

        return


    def draw(self, display):
        """Function draw takes in a display to be drawn onto. Animal is draw at size,
        and casted rays from the eye are drawn as well"""
        self.eye.draw(display)
        pygame.draw.circle(display, self.color, (self.x, self.y), self.size, 5)
        pygame.draw.circle(display, 'white', (self.x, self.y), self.size-5)