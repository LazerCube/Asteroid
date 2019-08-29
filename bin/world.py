import pygame
import random

import math

from utilites import util
from objects import objects

from objects.sprite import *
from objects.gui import *

class WorldState(object):
    objects = []
    n_objects = 0
    n_sprite = 0
    N_GUIobjects = 0

    def __init__(self, GameEngine):
        self.GameEngine = GameEngine

        #DEBUG variables
        self.DEBUG_MODE = self.GameEngine.DEBUG_MODE
        self.n_DEBUG_objects = 0

        self.once = True
        self.stateref = 0

        # MENU TOGGLE
        self.statechange = True

        # Collision map
        self.COLLISION_MAP_RESOLUTION = 100
        self.COLLISION_MAP_HEIGHT = int(math.ceil(float(self.GameEngine.Surface.HEIGHT) / self.COLLISION_MAP_RESOLUTION))
        self.COLLISION_MAP_WIDTH = int(math.ceil(float(self.GameEngine.Surface.WIDTH) / self.COLLISION_MAP_RESOLUTION))

        self.collision_map = []

        if self.DEBUG_MODE:
            objects.Debug(self)

        self.reset_world()

    def reset_world(self):
         # World variables
        self.objects = []
        self.n_objects = 0
        self.n_sprite = 0
        self.N_GUIobjects = 0

    def add(self, entitie):
        self.n_objects += 1
        self.objects.append(entitie)
        if self.DEBUG_MODE:
            print("Adding ", entitie)

    def remove(self, entitie):
        self.objects.remove(entitie)
        self.n_objects -= 1
        if self.DEBUG_MODE:
            print("Removing ", entitie)

    def handle_input(self):
        for i in self.objects:
            i.handle_input()

    def fixed_update(self):
        # Initalize map with empty values.
        self.collision_map = []
        for x in range(self.COLLISION_MAP_WIDTH):
            map_row = [[] for y in range(self.COLLISION_MAP_HEIGHT)]
            self.collision_map.append(map_row)

        for i in self.objects:
            i.fixed_update()

    def update(self, delta):
        for i in self.objects:
            i.update(delta)

    def render(self):
        for i in self.objects:
            i.draw()

class MenuState(WorldState):
    def __init__(self, GameEngine):
        super(MenuState, self).__init__(GameEngine)

        self.setup_menu()

    def setup_menu(self):
        label.Label(self, "MENU", 60, util.TERM_BLUE,
                            [self.GameEngine.Surface.WIDTH / 2, 50])

        button.PlayButton(self, "Play", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 225])

        button.ExitButton(self, "Exit To Desktop", 35, util.WHITE,
            [self.GameEngine.Surface.WIDTH / 2, 275])

        # button.Button(self, "Settings", 35, util.WHITE,
        #                     [self.GameEngine.Surface.WIDTH / 2, 275])

        # button.ExitButton(self, "Exit To Desktop", 35, util.WHITE,
        #                     [self.GameEngine.Surface.WIDTH / 2, 325])

        x = 200
        y = 450
        self.background_location = (((self.GameEngine.Surface.WIDTH / 2) - (x / 2)), 0, x, y)


    def handle_input(self):
        super(MenuState, self).handle_input()

    def fixed_update(self):
        super(MenuState, self).fixed_update()

    def update(self, delta):
        super(MenuState, self).update(delta)

    def render(self):
        self.GameEngine.Surface.SURFACE.fill(util.BLACK)
        super(MenuState, self).render()

class GameStateController():
    def __init__(self, GameEngine):
        self.GameEngine = GameEngine
        self.GAMESTATE = util.enum(GameState(GameEngine),
                                   PauseState(GameEngine))

        self.pause = False
        self.once = False
        self.set_game_state(0)

    def set_game_state(self, new_state):
        self.state = self.GAMESTATE.reverse_mapping[new_state]

    def handle_input(self):
        if(self.GameEngine.escape):
            self.GameEngine.escape = False
            if not (self.pause):
                self.set_game_state(1)
                self.pause = True
            else:
                self.set_game_state(0)
                self.pause = False

        self.state.handle_input()


    def fixed_update(self):
        self.state.fixed_update()

    def update(self, delta):
        self.state.update(delta)

    def render(self):
        self.state.render()


class GameState(WorldState):
    n_players = 0
    player = None
    n_asteroids = 0
    score = 0
    level = 1

    def __init__(self, GameEngine):
        super(GameState, self).__init__(GameEngine)

    def reset_world(self):
        super(GameState, self).reset_world()

        self.n_players = 0
        self.player = None
        self.n_asteroids = 0
        self.score = 0
        self.level = 1

        self.score_label = label.ValueLabel(self, "Score", 35, util.WHITE,
                        [self.GameEngine.Surface.WIDTH / 2, 35])

        self.level_label = label.ValueLabel(self, "Level", 35, util.WHITE,
                        [self.GameEngine.Surface.WIDTH / 2, 65], self.level)

        for i in range(0, 1):
            asteroid.Asteroid(self, random.randint(50,100),2)

        self.add_player()

    def add_player(self):
        if not (self.player):
            self.player = playership.PlayerShip(self)

    def handle_input(self):
        super(GameState, self).handle_input()

    def fixed_update(self):
        super(GameState, self).fixed_update()

    def update(self, delta):
        if self.player and not self.player.alive:
            self.player = None
            label.Label(self, "GAME OVER", 60, util.RED,
                        [self.GameEngine.Surface.WIDTH / 2, self.GameEngine.Surface.HEIGHT / 2])
            
            button.ResetButton(self, "Try again?", 40, util.WHITE,
                   [self.GameEngine.Surface.WIDTH / 2, (self.GameEngine.Surface.HEIGHT / 2) + 35])

        if self.n_asteroids is 0:
            for i in range(0, (2**self.level)):
                asteroid.Asteroid(self, random.randint(50,100),2)
            self.level += 1
            self.level_label.value = self.level

        self.score_label.value = self.score
        super(GameState, self).update(delta)

    def render(self):
        self.GameEngine.Surface.SURFACE.fill(util.BLACK)
        super(GameState, self).render()

class PauseState(WorldState):
    def __init__(self, GameEngine):
        super(PauseState, self).__init__(GameEngine)

        self.setup_menu()

    def setup_menu(self):
        label.Label(self, "PAUSE", 60, util.TERM_BLUE,
                            [self.GameEngine.Surface.WIDTH / 2, 50])

        button.Button(self, "Continue", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 300])

        button.ExitToMainMenuButton(self, "Exit to Main Menu", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 350])

        x = 250
        y = 450
        self.background_location = (((self.GameEngine.Surface.WIDTH / 2) - (x / 2)), 0, x, y)


    def handle_input(self):
        super(PauseState, self).handle_input()

    def fixed_update(self):
        super(PauseState, self).fixed_update()

    def update(self, delta):
        super(PauseState, self).update(delta)

    def render(self):
        pygame.draw.rect(self.GameEngine.Surface.SURFACE,(60,60,60), (self.background_location))
        super(PauseState, self).render()
