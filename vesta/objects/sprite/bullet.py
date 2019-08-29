import pygame
import random

from vesta.objects.objects import Sprite

class Bullet(Sprite):
    def __init__(self, world):
        super(Bullet, self).__init__(world)

        self.points = [[1,-4],[1,4],[1,4],[-1,4],[-1,4],[-1,-4]]
        self.scale = 1
        self.life = 100
        self.angle = 0

        self.collision = False

    def collide(self, other):
        pass

    def fixed_update(self):
        super(Bullet, self).fixed_update()

        self.life -= 1
        if(self.life == 0):
            self.kill()
