#!/usr/bin/python
import pygame
import world
import util


class _Game():
    def __init__(self, SURFACE):
        self.SURFACE = SURFACE
        self.world = world.World(SURFACE)
        self.width = self.world.WIDTH
        self.height = self.world.HEIGHT
        self._Run()

    def _Run(self):
        _MS_PER_TICK = 15.625
        _previous_time = pygame.time.get_ticks()
        _previous_timer = pygame.time.get_ticks()
        _current_time = 0

        frames = 0
        ticks = 0
        delta = 0

        while not(self.world.EXIT):
            _current_time = pygame.time.get_ticks()
            delta += ((_current_time - _previous_time) / _MS_PER_TICK)
            _previous_time = _current_time

            while(delta >= 1):
                self.world.update()
                ticks += 1
                delta -= 1

            self._Render()
            frames += 1

            if(pygame.time.get_ticks() - _previous_timer >= 1000):
                print("FPS: %i  TICKS: %i" % (frames, ticks))
                _previous_timer = pygame.time.get_ticks()
                frames = 0
                ticks = 0

    def _Render(self):
        self.SURFACE.fill(util.BLACK)
        self.world.render()

        pygame.display.flip()


def _Initiate():
    pygame.init()
    SURFACE = pygame.display.set_mode(
        [util.SURFACE_WIDTH, util.SURFACE_HEIGHT], pygame.HWSURFACE |
        pygame.DOUBLEBUF)
    pygame.display.set_caption(util.SURFACE_CAPTION)
    game = _Game(SURFACE)

    pygame.quit()

if __name__ == "__main__":
    _Initiate()
