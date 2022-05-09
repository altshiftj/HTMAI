from Wall import *


class Box:
    """
    Class Box defines the environment in which Animal moves. Box is composed of Walls.
    width - box width, defines pygame screen width as well
    height - box height
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # box is an array of walls
        self.walls = []

        # initial box border
        self.walls.append(Wall(0, 0, self.width, 0))
        self.walls.append(Wall(0, 0, 0, self.height))
        self.walls.append(Wall(self.width, 0, self.width, self.height))
        self.walls.append(Wall(0, self.height, self.width, self.height))


    def add_object(self, x1,y1, x2,y2):
        """Function add_object takes in four coordinates and constructs a box at this location"""
        self.walls.append(Wall(x1,y1 , x2,y1))
        self.walls.append(Wall(x2,y1 , x2,y2))
        self.walls.append(Wall(x2,y2 , x1,y2))
        self.walls.append(Wall(x1,y2 , x1,y1))


    def draw(self, display):
        """Function draw draws all walls within Box"""
        for wall in self.walls:
            wall.draw(display)
