import pygame

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

class GameState(WorldState):
    def __init__(self, GameEngine):
        super(GameState, self).__init__(GameEngine)
        self.n_players = 0

    def handleInput(self):
        super(GameState, self).handleInput()
        if (self.GameEngine.k_1):
            self.GameEngine.k_1 = False
            self.GameEngine.SetState(0)
        elif(self.GameEngine.keypad_0):
            self.GameEngine.keypad_0 = False
            playership.PlayerShip(self)
        elif(self.GameEngine.keypad_1):
            self.GameEngine.keypad_1 = False
            label.Label(self, "Test", 49, util.TERM_BLUE, [50, 50])

    def fixedUpdate(self):
        super(GameState, self).fixedUpdate()

    def update(self, delta):
        super(GameState, self).update(delta)

    def render(self):
        super(GameState, self).render()

class MenuState(WorldState):
    def __init__(self, GameEngine):
        super(MenuState, self).__init__(GameEngine)

        self.setupMenu()

    def setupMenu(self):
        label.Label(self, "MENU", 60, util.TERM_BLUE,
                            [self.GameEngine.Surface.WIDTH / 2, 30])

        button.PlayButton(self, "Play", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 300])

        button.Button(self, "Settings", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 350])

        button.Button(self, "Exit", 35, util.WHITE,
                            [self.GameEngine.Surface.WIDTH / 2, 400])

    def handleInput(self):
        super(MenuState, self).handleInput()
        if (self.GameEngine.k_2):
            self.GameEngine.k_2 = False
            self.GameEngine.SetState(1)

    def fixedUpdate(self):
        super(MenuState, self).fixedUpdate()

    def update(self, delta):
        super(MenuState, self).update(delta)
        print(self.GameEngine.k_up)

    def render(self):
        super(MenuState, self).render()
