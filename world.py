import pygame
import util

class World(object):
    def __init__(self, SURFACE):
        self.SURFACE = SURFACE
        self.WIDTH = SURFACE.get_width()
        self.HEIGHT = SURFACE.get_height()

        # Inputs
        self.quit = False

    def Update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = true

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit = event.type == pygame.KEYDOWN

    def draw(self):
        pass
