import random
from Brain import *
from Eye import *
from helpers.collisions import *

class Animal:

    def __init__(self, x, y, size, head_direction, field_of_view, color='white'):
        self.x = x
        self.y = y
        self.size = size
        self.head_direction = head_direction
        self.field_of_view = field_of_view
        self.brain = Brain()
        self.eye = Eye(x, y, head_direction, field_of_view)
        self.color = color
        collision = False

    def look(self, box):
        self.eye.see(box, self.x, self.y, self.head_direction)

    def think(self):
        self.brain.interpret(self.eye.vision)

    def move(self, step_size_move, box, direction):
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
        self.head_direction += step_size_turn

    def random_walk(self):
        pass

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.size)
        self.eye.draw(display)