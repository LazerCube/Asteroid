import pygame
import random

from utilites import util
from objects import objects

from objects.sprite import *
from objects.gui import *

class WorldState(object):
    def __init__(self, GameEngine):
        self.GameEngine = GameEngine

        #DEBUG variables
        self.DEBUG_MODE = self.GameEngine.DEBUG_MODE
        self.n_DEBUG_objects = 0

        self.once = True
        self.stateref = 0

        # MENU TOGGLE
        self.statechange = True

        # World variables
        self.objects = []
        self.n_objects = 0
        self.n_sprite = 0
        self.N_GUIobjects = 0

        if self.DEBUG_MODE:
            objects.Debug(self)

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

    def handleInput(self):
        for i in self.objects:
            i.handleInput()

    def fixedUpdate(self):
        for i in self.objects:
            i.fixedUpdate()

    def update(self, delta):
        for i in self.objects:
            i.update(delta)

    def render(self):
        for i in self.objects:
            i.Draw()

class MenuState(WorldState):
    def __init__(self, GameEngine):
        super(MenuState, self).__init__(GameEngine)

        self.setupMenu()

    def setupMenu(self):
        label.Label(self, "MENU", 60, util.TERM_BLUE,
                            [self.GameEngine.Surface.WIDTH / 2, 50])

        button.PlayButton(self, "Play", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 325])

        button.Button(self, "Settings", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 375])

        button.ExitButton(self, "Exit To Desktop", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 425])

        x = 200
        y = 450
        self.background_location = (((self.GameEngine.Surface.WIDTH / 2) - (x / 2)), 0, x, y)


    def handleInput(self):
        super(MenuState, self).handleInput()

    def fixedUpdate(self):
        super(MenuState, self).fixedUpdate()

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

    def handleInput(self):
        if(self.GameEngine.escape):
            self.GameEngine.escape = False
            if not (self.pause):
                self.set_game_state(1)
                self.pause = True
            else:
                self.set_game_state(0)
                self.pause = False

        self.state.handleInput()


    def fixedUpdate(self):
        self.state.fixedUpdate()

    def update(self, delta):
        self.state.update(delta)

    def render(self):
        self.state.render()


class GameState(WorldState):
    def __init__(self, GameEngine):
        super(GameState, self).__init__(GameEngine)
        self.n_players = 0
        self.player = None

        #Asteroid information
        self.n_asteroids = 0

        self.addPlayer()

        for i in range(0, 5):
            asteroid.Asteroid(self, random.randint(50,100),5)

    def addPlayer(self):
        if not (self.player):
            self.player = playership.PlayerShip(self)

    def handleInput(self):
        super(GameState, self).handleInput()

    def fixedUpdate(self):
        super(GameState, self).fixedUpdate()

    def update(self, delta):
        super(GameState, self).update(delta)

    def render(self):
        self.GameEngine.Surface.SURFACE.fill(util.BLACK)
        super(GameState, self).render()

class PauseState(WorldState):
    def __init__(self, GameEngine):
        super(PauseState, self).__init__(GameEngine)

        self.setupMenu()

    def setupMenu(self):
        label.Label(self, "PAUSE", 60, util.TERM_BLUE,
                            [self.GameEngine.Surface.WIDTH / 2, 50])

        button.Button(self, "Continue", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 300])

        button.ExitToMainMenuButton(self, "Exit to Main Menu", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 400])

        x = 250
        y = 450
        self.background_location = (((self.GameEngine.Surface.WIDTH / 2) - (x / 2)), 0, x, y)


    def handleInput(self):
        super(PauseState, self).handleInput()

    def fixedUpdate(self):
        super(PauseState, self).fixedUpdate()

    def update(self, delta):
        super(PauseState, self).update(delta)

    def render(self):
        pygame.draw.rect(self.GameEngine.Surface.SURFACE,(60,60,60), (self.background_location))
        super(PauseState, self).render()
