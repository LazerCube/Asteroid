import pygame

from utilites import util
from objects import objects

class PlayerShip(objects.Sprite):
    def __init__(self, world):
        super(PlayerShip, self).__init__(world)
        self.position = [self.worldstate.world.WIDTH / 2,
                         self.worldstate.world.HEIGHT / 2]
        self.points = [[0, 0], [-5, 5],
                       [-5, 5], [0, -10],
                       [0, -10], [5, 5],
                       [5, 5], [0, 0]]
        self.hitbox = [[-5, -10], [5, -10],
                       [5, -10], [5, 5],
                       [5, 5], [-5, 5],
                       [-5, 5], [-5, -10]]

        self.name = "TEST"
        self.velocity = [0, 0]
        self.scale = 2
        self.hover = True

        self.speed = 1
        self.rotate_speed = 4

        # Inputs
        self.rotate_left = False
        self.rotate_right = False
        self.thrust = False

        self.UpdateHitBox()
        world.n_players += 1

    def rotate_by(self, rot):
        self.angle += rot
        self.angle %=360

    def HandleInput(self):
        super(PlayerShip, self).HandleInput()
        self.thrust = self.worldstate.k_up
        self.rotate_left = self.worldstate.k_left
        self.rotate_right = self.worldstate.k_right

    def Update(self):
        if self.thrust:
            u = (self.speed * util.cos(self.angle - 90))
            v = (self.speed * util.sin(self.angle - 90))
            self.velocity = [(self.velocity[0] + u), (self.velocity[1] + v)]
        if self.rotate_left:
            self.rotate_speed = 4
            self.rotate_by(- self.rotate_speed)
        elif self.rotate_right:
            self.rotate_by(self.rotate_speed)

        super(PlayerShip, self).Update()


    def Draw(self, delta):
        super(PlayerShip, self).Draw(delta)
