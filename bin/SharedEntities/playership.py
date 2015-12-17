import pygame
import sprite
import util


class PlayerShip(sprite.Sprite):
    def __init__(self, world):
        super(PlayerShip, self).__init__(world)
        self.position = [self.worldstate.world.WIDTH / 2,
                         self.worldstate.world.HEIGHT / 2]
        self.points = [[0, 0], [-5, 5],
                       [-5, 5], [0, -10],
                       [0, -10], [5, 5],
                       [5, 5], [0, 0]]
        self.name = "TEST"
        self.velocity = [1, 1]
        self.scale = 4

        world.n_players += 1

    def handleInput(self):
        if(self.worldstate.k_a):
            self.scale += 1
        elif(self.worldstate.k_d):
            self.scale -= 1

    def Update(self):
        super(PlayerShip, self).Update()
        self.angle += 1

    def Draw(self):
        super(PlayerShip, self).Draw()
