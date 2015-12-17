import entities

import pygame
import util


class Sprite(entities.Entities):
    def __init__(self, world):
        super(Sprite, self).__init__(world)
        world.n_sprite += 1
        self.velocity = [0, 0]
        self.points = []

    def handleInput(self):
        super(Sprite, self).handleInput()

    def Update(self):
        super(Sprite, self).Update()
        self.position = [self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1]]

        self.position[0] %= self.worldstate.world.WIDTH
        self.position[1] %= self.worldstate.world.HEIGHT

    def Draw(self):
        super(Sprite, self).Draw()
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        screen_points = [[int(a * x + b * y + self.position[0]),
                          int(c * x + d * y + self.position[1])]
                         for x, y in self.points]

        pygame.draw.lines(self.worldstate.world.SURFACE,
                          self.color, True, screen_points)
