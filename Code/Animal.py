import random   #for random walk
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
    def __init__(self, x, y, size, head_direction, field_of_view, color='white'):
        self.x = x
        self.y = y
        self.size = size
        self.head_direction = head_direction
        self.field_of_view = field_of_view
        self.eye = Eye(x, y, head_direction, field_of_view, size, 1200, 10)
        self.brain = Brain(self.eye)
        self.color = color


    def look(self, box):
        """Function look takes in an environment and looks at it using Eye at Animal x and y in head_direction"""
        self.eye.see(box, self.x, self.y, self.head_direction)


    def think(self):
        """Function think passes encoded Eye SDR to Brain for Spatial Pooling and Temporal Memory functions"""
        self.brain.thought_count+=1
        self.brain.encode(self.eye)
        self.brain.pool()
        self.brain.temporal()


    def move(self, step_size_move, box, direction):
        """Function move takes in a step size (speed), environment, and forward or backward direction
        to define movement. Animal moves within the environment checking for collisions as it goes"""
        if direction == 'forward':

            for wall in box.walls:
                collision = move_collision(self, wall, True)
                if collision:
                    break

            if not collision:
                self.x += step_size_move * math.cos(math.radians(self.head_direction))
                self.y += step_size_move * math.sin(math.radians(self.head_direction))


        if direction == 'backward':
            for wall in box.walls:
                collision = move_collision(self, wall, False)
                if collision:
                    break
            if not collision:
                self.x -= step_size_move * math.cos(math.radians(self.head_direction))
                self.y -= step_size_move * math.sin(math.radians(self.head_direction))


    def turn(self, step_size_turn):
        """Function turn takes in a step size (angular speed) and augments head direction accordingly
        (CW+ convention)"""
        #self.eye.direction = self.head_direction
        if (self.head_direction + step_size_turn)>=360:
            self.head_direction -= 360
        elif (self.head_direction + step_size_turn) < 0:
            self.head_direction += 360

        self.head_direction+=step_size_turn
        return



    def random_walk(self):
        """Function random_walk defines a method of random motion for Animal"""
        pass


    def draw(self, display):
        """Function draw takes in a display to be drawn onto. Animal is draw at size,
        and casted rays from the eye are drawn as well"""
        pygame.draw.circle(display, self.color, (self.x, self.y), self.size)
        self.eye.draw(display)