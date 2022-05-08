from Wall import *


class Box:
    # default constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.walls = []
        self.walls.append(Wall(0, 0, self.width, 0))
        self.walls.append(Wall(0, 0, 0, self.height))
        self.walls.append(Wall(self.width, 0, self.width, self.height))
        self.walls.append(Wall(0, self.height, self.width, self.height))

    def add_object(self, x1,y1, x2,y2):
        self.walls.append(Wall(x1,y1 , x2,y1))
        self.walls.append(Wall(x2,y1 , x2,y2))
        self.walls.append(Wall(x2,y2 , x1,y2))
        self.walls.append(Wall(x1,y2 , x1,y1))

    def draw(self, display):
        for wall in self.walls:
            wall.draw(display)
