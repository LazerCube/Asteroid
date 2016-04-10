import pygame
import random

from utilites import util
from objects import objects

class Bullet(objects.Sprite):
    def __init__(self, world):
        super(Bullet, self).__init__(world)

        self.points = [[1,-4],[1,4],[1,4],[-1,4],[-1,4],[-1,-4]]
        self.scale = 1
        self.life = 100
        self.angle = 0

    def fixedUpdate(self):
        super(Bullet, self).fixedUpdate()

        self.life -= 1
        if(self.life == 0):
            self.kill =True
