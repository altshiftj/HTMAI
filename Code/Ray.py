import pygame
import math

class Ray:

    def __init__(self, x, y, angle, color='white'):
        self.x1 = x
        self.y1 = y

        self.angle = math.radians(angle)
        self.length = 1

        self.x2 = self.x1 + self.length * math.cos(self.angle)
        self.y2 = self.y1 + self.length * math.sin(self.angle)

        self.color = color

    def update(self, x, y, angle):
        self.x1 = x
        self.y1 = y
        self.angle = math.radians(angle)

    def update_end_point(self):
        self.x2 = self.x1 + self.length * math.cos(self.angle)
        self.y2 = self.y1 + self.length * math.sin(self.angle)

    def draw(self, display):
        pygame.draw.line(display, self.color, (self.x1,self.y1) , (self.x2,self.y2))
