import pygame

from utilites import util
from objects import objects

from objects.sprite import bullet

class PlayerShip(objects.Sprite):
    def __init__(self, world):
        super(PlayerShip, self).__init__(world)
        self.world = world
        self.position = [self.GameEngine.Surface.WIDTH / 2,
                         self.GameEngine.Surface.HEIGHT / 2]
        self.points = [[0, 0], [-5, 5],
                       [-5, 5], [0, -10],
                       [0, -10], [5, 5],
                       [5, 5], [0, 0]]
        self.hitbox = [[-5, -10], [5, -10],
                       [5, -10], [5, 5],
                       [5, 5], [-5, 5],
                       [-5, 5], [-5, -10]]

        self.hover = False

        self.name = "PlayerShip"
        self.velocity = [0, 0]
        self.scale = 1.25

        #Movement variables
        self.max_velocity = 25
        self.speed = 0.25
        self.rotate_speed = 4

        # Inputs
        self.rotate_left = False
        self.rotate_right = False
        self.thrust = False

        self.primary_fire = False

        #Reloading
        self.reload_timer = False
        self.reload_timer = 0

        world.n_players += 1

    def fire(self):
        if(self.reload_timer == 0):
            a = util.cos(self.angle - 90)
            b = util.sin(self.angle - 90)

            projectile = bullet.Bullet(self.world)
            projectile.position = [self.position[0] + self.scale * a,
                                    self.position[1] + self.scale * b]
            projectile.velocity = [a * 7.0 + self.velocity[0],
                                    b * 7.0 + self.velocity[1]]
            projectile.angle = self.angle

            self.reload_timer = 10


    def handle_input(self):
        super(PlayerShip, self).handle_input()

        self.thrust = self.GameEngine.k_up
        self.rotate_left = self.GameEngine.k_left
        self.rotate_right = self.GameEngine.k_right
        self.primary_fire = self.GameEngine.k_space

    def fixed_update(self):
        if self.rotate_left:
            self.angular_velocity = (- self.rotate_speed)
        elif self.rotate_right:
            self.angular_velocity = (self.rotate_speed)
        else:
            self.angular_velocity = 0

        if self.thrust:
            u = (self.speed * util.cos(self.angle - 90))
            v = (self.speed * util.sin(self.angle - 90))
            self.velocity = [(self.velocity[0] + u), (self.velocity[1] + v)]

        if self.primary_fire:
            self.fire()

        self.reload_timer = max(0, self.reload_timer - 1)

        super(PlayerShip, self).fixed_update()

    def draw(self):
        super(PlayerShip, self).draw()
