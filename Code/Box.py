from Wall import *
from helpers.geometry import *
import random


class Box:
    """
    Class Box defines the environment in which Animal moves. Box is composed of Walls.
    width - box width, defines pygame screen width as well
    height - box height
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.seed_count=1

        # box is an array of walls
        self.walls = []

        self.color_divider = 8

        # initial box border
        self.create_borders()

    def create_borders(self):
        """Create the borders of the box."""
        self.add_wall(0, 0, self.width, 0)
        self.add_wall(0, 0, 0, self.height)
        self.add_wall(self.width, 0, self.width, self.height)
        self.add_wall(0, self.height, self.width, self.height)

    def add_object(self, x1, y1, x2, y2):
        """Add an object as a set of walls at the specified coordinates."""
        self.walls.extend([
            Wall(x1, y1, x2, y1),
            Wall(x2, y1, x2, y2),
            Wall(x2, y2, x1, y2),
            Wall(x1, y2, x1, y1)
        ])

    def add_wall(self,x1,y1, x2,y2):
        """Add a wall with color transitions between the given coordinates."""
        xdist = x2-x1
        ydist = y2-y1
        for i in range(self.color_divider):
            self.walls.append(Wall(x1 + i * xdist / self.color_divider,
                                   y1 + i * ydist / self.color_divider,
                                   x1 + (i + 1) * xdist / self.color_divider,
                                   y1 + (i + 1) * ydist / self.color_divider,
                                   self.generate_random_color()))

    def draw(self, display):
        """Function draw draws all walls within Box"""
        for wall in self.walls:
            wall.draw(display)

    def generate_random_color(self):
        random.seed(self.seed_count)
        random_color = random.randint(1,6)
        return random_color

