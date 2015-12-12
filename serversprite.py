import copy

import util
import math

class ServerSprite(object):
    def __init__(self, game):
        self.game = game
        self.position = [0,0]
        self.velocity = [0,0]
        self.points = []
        self.screen_points = []

        self.kill = False
        self.scale = 10
        self.angle = 0

        game.add(self)

    def update(self):
        self.position = [self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1]]

        self.position[0] %= self.game.width
        self.position[1] %= self.game.height

    def draw(self):

        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        screen_points = [[int(a * x + b * y + self.position[0]),
                          int(c * x + d * y + self.position[1])]
                         for x, y in self.points]
