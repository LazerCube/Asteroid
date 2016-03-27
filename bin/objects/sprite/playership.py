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

    def Update(self):
        super(PlayerShip, self).Update()

    def Draw(self):
        super(PlayerShip, self).Draw()
