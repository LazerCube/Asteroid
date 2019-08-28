import pygame
import random

from utilites import util
from objects import objects

from objects.sprite import bullet
from objects.particles.explosion import Explosion

class Asteroid(objects.Sprite):
    def __init__(self, world, scale, max_speed):
            super(Asteroid, self).__init__(world)
            world.n_asteroids += 1

            self.angle = 0
            self.scale = scale
            self.angular_velocity = 0

            self.update_hit_box()
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

    def collide(self, other):
        if isinstance(other, Asteroid):
            new_angular_velocity = other.angular_velocity
            other.angular_velocity = self.angular_velocity
            self.angular_velocity = new_angular_velocity

        super(Asteroid, self).collide(other)

    def impact(self, other):
        if isinstance(other, bullet.Bullet):
            # self.world.particle.explosion(10, self.position, self.velocity, 10, 35)
            self.worldstate.score += self.scale
            
            other.kill()
            self.kill()

            if self.scale > 15:
                n = random.randint(2, max(2, min(5, self.scale / 5)))
                for i in range(n):
                    new_asteroid = Asteroid(self.worldstate, self.scale / n, 1)
                    new_asteroid.position[0] = self.position[0]
                    new_asteroid.position[1] = self.position[1]
                    new_asteroid.velocity[0] += self.velocity[0]
                    new_asteroid.velocity[1] += self.velocity[1]

    def kill(self):
        self.worldstate.n_asteroids -= 1
        Explosion(self.worldstate, self.color, self.position, self.velocity)
        super(Asteroid ,self).kill()

    def fixed_update(self):
        super(Asteroid, self).fixed_update()
