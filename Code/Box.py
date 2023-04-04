from Wall import *
from helpers.geometry import *
import random


class Box:
    """
    Class Box defines the environment in which Animal moves. Box is composed of Walls.

    :param width    (int): box width, defines pygame screen width as well
    :param height   (int): box height
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.seed_count=1

        # box is an array of walls
        self.walls = []

        # box walls are divided into a set number of colors
        self.color_divider = 8

        # initial box border
        self.add_wall(0, 0, self.width, 0)
        self.add_wall(0, 0, 0, self.height)
        self.add_wall(self.width, 0, self.width, self.height)
        self.add_wall(0, self.height, self.width, self.height)


    def add_object(self, x1,y1, x2,y2):
        """
        Function add_object takes in four coordinates and constructs a box at this location

        :param x1   (int): x coordinate of first point
        :param y1   (int): y coordinate of first point
        :param x2   (int): x coordinate of second point
        :param y2   (int): y coordinate of second point
        """
        self.walls.append(Wall(x1,y1 , x2,y1))
        self.walls.append(Wall(x2,y1 , x2,y2))
        self.walls.append(Wall(x2,y2 , x1,y2))
        self.walls.append(Wall(x1,y2 , x1,y1))

    def add_wall(self,x1,y1, x2,y2):
        """
        Function add_wall takes in four coordinates and constructs a wall at those start and end points

        :param x1   (int): x coordinate of first point
        :param y1   (int): y coordinate of first point
        :param x2   (int): x coordinate of second point
        :param y2   (int): y coordinate of second point
        :return:
        """
        xdist = x2-x1
        ydist = y2-y1
        for i in range(self.color_divider):
            self.walls.append(Wall(x1+i*xdist/self.color_divider,
                                   y1+i*ydist/self.color_divider,
                                   x1+(i+1)*xdist/self.color_divider,
                                   y1+(i+1)*ydist/self.color_divider,
                                   self.generate_random_color()))

    def draw(self, display):
        """Function draw draws all walls within Box"""
        for wall in self.walls:
            wall.draw(display)

    def generate_random_color(self):
        """
        Function generate_random_color generates a random number dictating the color of a wall
        """
        random.seed(self.seed_count)
        random_color = random.randint(1,6)
        self.seed_count+=1
        return random_color

