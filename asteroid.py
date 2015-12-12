import pygame
import math
import random

import util
import serversprite

class Asteroid(serversprite.ServerSprite):
    def __init__(self, game, scale, max_speed):
        super(Asteroid, self).__init__(game)
        game.n_asteroids += 1

        if random.randint(0,1) == 0:
            x = random.randint(0, game.width)
            y = random.randint(0,1)  * game.height
        else:
            x = random.randint(0, 1) * game.width
            y = random.randint(0 , game.height)
        self.position = [x, y]

        n_points = random.randint(5,10)
        self.points = []
        for i in range(n_points):
            angle = i * 360 / n_points + random.randint(-20,20)
            distance = random.random() / 4.0 + 0.75
            self.points.append([distance * util.cos(angle),
                                distance * util.sin(angle)])

        self.velocity = [random.random() * max_speed * 2 - max_speed,
                         random.random() * max_speed * 2 - max_speed]

        self.angle = 0
        self.scale = scale
        self.angular_velocity =  random.random() * 4 - 2

    def collide(self, other):
        pass

    def update(self):
        self.angle += self.angular_velocity
        super(Asteroid, self).update()
