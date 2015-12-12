import pygame
import copy

import util
import math

class Sprite(object):
    def __init__(self, world):
        self.world = world
        self.position = [0,0]
        self.velocity = [0,0]
        self.points = []
        self.screen_points = []

        self.kill = False
        self.scale = 10
        self.angle = 0

        self.team_color = util.WHITE

        world.add(self)

    def test_collisions(self, possible_sprites):
        pass

    def collide(self, other):
        pass

    def impact(self, other):
        pass

    def update(self):
        self.position = [self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1]]

        self.position[0] %= self.world.width
        self.position[1] %= self.world.height

    def draw(self):

        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        screen_points = [[int(a * x + b * y + self.position[0]),
                          int(c * x + d * y + self.position[1])]
                         for x, y in self.points]

        pygame.draw.lines(self.world.surface, self.team_color, True, screen_points)
