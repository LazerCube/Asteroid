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
        self.rotate_by = 0
        self.scale = 2
        self.hover = False

        # Inputs
        self.rotate_left = False
        self.rotate_right = False

        self.updatehitbox()
        world.n_players += 1

    def handleInput(self):
        super(PlayerShip, self).handleInput()
        if(self.worldstate.up):
            self.thrust()
        if(self.worldstate.left):
            self.rotate_by = -4
        elif(self.worldstate.right):
            self.rotate_by = 4
        else:
            self.rotate_by = 0

    def Update(self):
        self.rotate(self.rotate_by)
        super(PlayerShip, self).Update()

    def thrust(self):
        u = 0.1 * util.cos(self.angle - 90)
        v = 0.1 * util.sin(self.angle - 90)
        self.velocity = [self.velocity[0] + u, self.velocity[1] + v]

    def rotate(self, angle):
        self.angle += angle
        self.angle %=360

    def Draw(self):
        super(PlayerShip, self).Draw()
