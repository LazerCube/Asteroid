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

        # Inputs
        self.rotate_left = False
        self.rotate_right = False
        self.thrust = False

        self.rotate_speed = 4

        self.updatehitbox()
        world.n_players += 1

    def rotate_by(self, angle):
        self.angle += angle
        self.angle %=360

    def handleInput(self):
        super(PlayerShip, self).handleInput()
        self.thrust = self.worldstate.k_up
        self.rotate_left = self.worldstate.k_left
        self.rotate_right = self.worldstate.k_right

    def Update(self):
        super(PlayerShip, self).Update()
        if self.rotate_left:
            self.rotate_by(- self.rotate_speed)
        elif self.rotate_right:
            self.rotate_by(self.rotate_speed)
        else:
            self.rotate_by(0)
        if self.thrust:
            u = 0.1 * util.cos(self.angle - 90)
            v = 0.1 * util.sin(self.angle - 90)
            self.velocity = [self.velocity[0] + u, self.velocity[1] + v]


    def Draw(self):
        super(PlayerShip, self).Draw()
