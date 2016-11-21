import pygame
import random

from utilites import util
from objects import objects

class Asteroid(objects.Sprite):
    def __init__(self, world, scale, max_speed):
            super(Asteroid, self).__init__(world)
            world.n_asteroids += 1

            self.angle = 0
            self.scale = scale
            self.angular_velocity = 0

            self.updateHitBox()
            self.generate(max_speed)

    def generate(self, max_speed):
        if random.randint(0,1) == 0:
            x = random.randint(0, self.GameEngine.Surface.WIDTH)
            y = random.randint(0,1)  * self.GameEngine.Surface.HEIGHT
        else:
            x = random.randint(0, 1) * self.GameEngine.Surface.WIDTH
            y = random.randint(0 , self.GameEngine.Surface.HEIGHT)
        self.position = [x, y]

        n_points = random.randint(5,10)

        for i in range(n_points):
            angle = i * 360 / n_points + random.randint(-20,20)
            distance = random.random() / 4.0 + 0.75
            self.points.append([distance * util.cos(angle),
                                distance * util.sin(angle)])

        self.velocity = [random.random() * max_speed * 2 - max_speed,
                         random.random() * max_speed * 2 - max_speed]

        self.angular_velocity =  random.random() * 5 - 2

    def fixedUpdate(self):
        super(Asteroid, self).fixedUpdate()
