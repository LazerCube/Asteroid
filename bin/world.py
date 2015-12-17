import SharedEntities.guiobjects  # import for all game states
import SharedEntities.sprite

import pygame
import util


class WorldState(object):
    def __init__(self, world):
        self.world = world
        self.entities = []
        self.n_entities = 0
        self.n_sprite = 0
        self.N_GUIobjects = 0

        # objects
        self.sprite = SharedEntities.sprite
        self.guiobjects = SharedEntities.guiobjects

        # Events
        self.resize = False

        # Inputs
        self.escape = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.k_a = False
        self.k_d = False

    def add(self, entitie):
        self.n_entities += 1
        self.entities.append(entitie)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.world.EXIT = True

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.world.EXIT = True
                elif event.key == pygame.K_LEFT:
                    self.left = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RIGHT:
                    self.right = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_DOWN:
                    self.down = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_UP:
                    self.up = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_a:
                    self.k_a = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_d:
                    self.k_d = event.type == pygame.KEYDOWN

        for i in self.entities:
            i.handleInput()

    def update(self):
        self.handleInput()
        for i in self.entities:
            i.Update()

    def render(self):
        for i in self.entities:
            i.Draw()
