import random

from vesta.utilites import util
from vesta.objects.objects import ParticleSystem

class Explosion(ParticleSystem):
    def __init__(self, world, color, position, velocity, particle_speed=4, n_points=10, min_life=10, max_life=35):
        super(Explosion, self).__init__(world, color, position)

        for i in range(n_points):
            delta = 360.0 / n_points
            angle = i * delta + random.randint(int(-delta), int(delta))
            speed = random.random() * particle_speed 
            self.add([velocity[0] + speed * util.cos(angle - 90),
                      velocity[1] + speed * util.sin(angle - 90)],
                      random.randint(min_life, max_life))