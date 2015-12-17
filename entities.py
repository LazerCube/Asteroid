import pygame
import util


class Entities(object):
    def __init__(self, world):
        self.worldstate = world
        self.name = None
        self.position = [0, 0]
        self.hitbox = [[0, 0], [1, 0],
                       [1, 0], [1, 1],
                       [1, 1], [0, 1],
                       [0, 1], [1, 1]]
        self.kill = False
        self.scale = 10
        self.angle = 0
        self.color = util.WHITE
        self.worldstate.add(self)

    def Update(self):
        pass

    def Draw(self):
        pass
