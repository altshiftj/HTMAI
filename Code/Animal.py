from Brain import *
from Eye import *
from helpers.collisions import *
from Code.helpers.cells_to_csv import *

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
    def __init__(self, x, y, size, head_direction, field_of_view, num_of_rays, color='white'):
        self.x = x
        self.y = y
        self.linear_speed = 0
        self.angular_velocity = 0

        self.size = size

        self.head_direction = head_direction
        self.field_of_view = field_of_view

        self.eye = Eye(x, y, head_direction, field_of_view, size, 1200, num_of_rays)
        self.brain = Brain(self.eye, metrics_on=True)

        self.color = color


    def look(self, box):
        """Function look takes in an environment and looks at it using Eye at Animal x and y in head_direction"""
        self.eye.see(box, self.x, self.y, self.head_direction)


    def think(self):
        """Function think passes encoded Eye SDR to Brain for Spatial Pooling and Temporal Memory functions"""
        if self.brain.thought_count == 0:
            self.brain.thought_count += 1
            initialize_csv()
            self.brain.encode_movement(self.linear_speed, self.angular_velocity)
            self.brain.pool_movement()
            self.brain.temporal_location()

            self.brain.encode_vision(self.eye)
            self.brain.pool_senses()
            self.brain.temporal_senses()

        self.brain.thought_count += 1

        self.brain.encode_movement(self.linear_speed, self.angular_velocity)
        self.brain.pool_movement()
        self.brain.temporal_location()

        self.brain.temporal_senses_motion_context()

        self.brain.encode_vision(self.eye)
        self.brain.pool_senses()
        self.brain.temporal_senses()

        self.brain.temporal_location_sensory_context()

        self.brain.pool_object()
        self.brain.temporal_object()

        self.brain.temporal_senses_object_context()

        if self.brain.thought_count > 50000:
            write_activecell_to_csv(self.brain.L6a_location_tm,
                                    'L6a_active',
                                    self.brain.thought_count,
                                    int(self.x),
                                    int(self.y),
                                    int(self.head_direction),
                                    self.linear_speed,
                                    self.angular_velocity)

            write_activecell_to_csv(self.brain.L4_sensory_tm,
                                    'L4_active',
                                    self.brain.thought_count,
                                    int(self.x),
                                    int(self.y),
                                    int(self.head_direction),
                                    '-','-')

            write_activecell_to_csv(self.brain.L23_object_tm,
                                    'L23_active',
                                    self.brain.thought_count,
                                    int(self.x),
                                    int(self.y),
                                    int(self.head_direction),
                                    '-', '-')

        self.linear_speed = 0
        self.angular_velocity = 0
        return


    def move(self, step_size_move, box, direction):
        """Function move takes in a step size (speed), environment, and forward or backward direction
        to define movement. Animal moves within the environment checking for collisions as it goes"""
        if direction == 'forward':

            for wall in box.walls:
                collision = move_collision(self, wall, True)
                if collision:
                    break

            if not collision:
                self.linear_speed += step_size_move
                self.x += step_size_move * math.cos(math.radians(self.head_direction))
                self.y += step_size_move * math.sin(math.radians(self.head_direction))

        if direction == 'backward':
            for wall in box.walls:
                collision = move_collision(self, wall, False)
                if collision:
                    break

            if not collision:
                self.linear_speed += -step_size_move
                self.x -= step_size_move * math.cos(math.radians(self.head_direction))
                self.y -= step_size_move * math.sin(math.radians(self.head_direction))


    def turn(self, xdir, ydir):

        if xdir==0:
            xdir+=.01

        theta = math.degrees(math.atan2(ydir,xdir))
        if theta < 0:
            theta+=360

        if abs((theta - self.head_direction))>180 and theta>self.head_direction:
            self.angular_velocity += (theta - (self.head_direction+360))
        elif abs((theta - self.head_direction))>180 and theta<self.head_direction:
            self.angular_velocity += ((theta+360) - self.head_direction)
        else:
            self.angular_velocity += (theta - self.head_direction)

        self.head_direction = theta

        if self.head_direction < 0:
            self.head_direction += 360

        return
        # if (self.head_direction + step_size_turn)>=360:
        #     self.head_direction -= 360
        # elif (self.head_direction + step_size_turn) < 0:
        #     self.head_direction += 360
        #
        # self.head_direction += step_size_turn
        # self.angular_velocity += step_size_turn


    def draw(self, display):
        """Function draw takes in a display to be drawn onto. Animal is draw at size,
        and casted rays from the eye are drawn as well"""
        self.eye.draw(display)
        pygame.draw.circle(display, self.color, (self.x, self.y), self.size)