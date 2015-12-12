#!/usr/bin/python

import pygame
import time
import random
import sys

import util
import world

class Game():
    def __init__(self, surface):
        self.surface = surface
        self.world = world.World(surface)
        self.width = self.world.width
        self.height = self.world.height
        self.fps_info = None
        self.uncapped_fps = True


    def draw_hud(self): # draws the HUD
        self.surface.blit(self.world.add_text(("Score: %i" %self.world.score), "hud"), (self.world.width / 2  -40 ,5))
        self.surface.blit(self.world.add_text(("Player: %i" %(self.world.num + 1)), "hud"), (self.world.width / 2  -42 ,30))

    def draw_info(self):
        if self.world.info:
            self.surface.blit(self.world.add_text(self.fps_info, "info"), (5,5))
            self.surface.blit(self.world.add_text(("Objects: %i" %self.world.n_sprites), "info"), (150,5))


    def play_game(self):
        self.world.add_player()
        self.play_level()

    def play_level(self):
        msPerTick = 15.625
        lastTimer = pygame.time.get_ticks()
        lastCurrentTime = pygame.time.get_ticks()

        frames = 0
        ticks = 0
        delta = 0

        while self.world.quit == False:
            currentTime = pygame.time.get_ticks()
            delta +=((currentTime - lastCurrentTime)/msPerTick)
            lastCurrentTime = currentTime

            self.doesrender = self.uncapped_fps

            while (delta >= 1 ):
                ticks += 1
                self.world.update()
                self.doesrender = True
                delta -= 1

            if self.doesrender == True:
                self.on_render()# renders everything.
                frames += 1

            if(pygame.time.get_ticks() - lastTimer >= 1000):
                lastTimer += 1000
                self.update_fps(ticks, frames)
                frames = 0
                ticks = 0

    def on_render(self):#renders everything
        self.surface.fill(util.BLACK)
        self.draw_hud()
        self.draw_info()
        self.world.draw()
        pygame.display.flip()


    def update_fps(self, ticks, frames):#updates fps every second
        self.fps_info = "Ticks: %i  Frames:  %i " %(ticks, frames)
        ticks == 0
        frames = 0


def main():
    pygame.init()
    surface = pygame.display.set_mode([util.display_width,util.display_height], pygame.HWSURFACE | pygame.DOUBLEBUF)
    #pygame.mouse.set_visible(False) # sets the mouse to invisible
    pygame.display.set_caption("Game Engine") # set the title for the window

    game = Game(surface)
    game.play_game()

    pygame.quit()
    print("Exiting Window")
    sys.exit

if __name__ == "__main__":
    main()
