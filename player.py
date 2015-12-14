import pygame
import math

import util
import sprite

class player(sprite.Sprite):
    def __init__(self, world):
        super(player,self).__init__(world)

        self.position = [world.width / 2,
                         world.height / 2]

        self.points = [[0,0],[-5,5],[-5,5],[0,-10],[0,-10],[5,5],[5,5],[0,0]]

        self.velocity = [0,0]
        self.scale = 1
        self.angle = 0


    def rotate_by(self, angle):
        self.angle += angle
        self.angle %=360

    def thrust(self):
        u = 0.1 * util.cos(self.angle - 90)
        v = 0.1 * util.sin(self.angle - 90)
        self.velocity = [self.velocity[0] + u, self.velocity[1] + v]

    def update(self):
        super(player,self).update()

    def impact(self, other):
        pass

    def collide(self, other):
        pass

    def draw(self):
        super(player,self).draw()
