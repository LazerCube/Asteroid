import pygame
import util


class Entities(object):
    def __init__(self, world):
        self.worldstate = world
        self.name = None
        self.position = [0, 0]
        self.hitbox = [[-1, -1], [-1, 1],
                       [-1, 1], [1, 1],
                       [1, 1], [1, -1],
                       [1, -1], [-1, -1]]
        self.hitbox_pos = []
        self.kill = False
        self.scale = 10
        self.angle = 0
        self.color = util.WHITE
        self.worldstate.add(self)
        self.hover = False

    def updatehitbox(self):
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        self.hitbox_pos = [[int(a * x + b * y + self.position[0]),
                            int(c * x + d * y + self.position[1])]
                           for x, y in self.hitbox]

    def handleInput(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pygame.draw.lines(self.worldstate.world.SURFACE,
                          util.GREEN, True, self.hitbox_pos)
