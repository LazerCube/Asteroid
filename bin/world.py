import pygame

from utilites import util
from objects import objects

from objects.sprite import *
from objects.gui import *

class WorldState(object):
    def __init__(self, world):
        self.world = world

        #DEBUG variables
        self.DEBUG_MODE = self.world.DEBUG_MODE
        self.n_DEBUG_objects = 0

        # World variables
        self.objects = []
        self.n_objects = 0
        self.n_sprite = 0
        self.N_GUIobjects = 0

        # Events
        self.resize = False

        # Keyboard Inputs
        self.escape = False
        self.delete = False
        self.k_left = False
        self.k_right = False
        self.k_up = False
        self.k_down = False
        self.k_a = False
        self.k_d = False

        # Keyboard Numberpad
        self.keypad_0 = False
        self.keypad_1 = False
        self.keypad_2 = False
        self.keypad_3 = False
        self.keypad_4 = False
        self.keypad_5 = False
        self.keypad_6 = False
        self.keypad_7 = False
        self.keypad_8 = False
        self.keypad_9 = False

        # Keyboard Number row
        self.k_0 = False
        self.k_1 = False
        self.k_2 = False
        self.k_3 = False

        # Mouse Inputs
        self.mouse_pressed = [False, False, False]
        self.mouse_pos = [0, 0]

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
        for event in pygame.event.get():
            pygame.event.pump()
            if event.type == pygame.QUIT:
                self.world.EXIT = True
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.mouse_pressed)):
                    if pygame.mouse.get_pressed()[i]:
                        self.mouse_pressed[i] = True
                    else:
                        self.mouse_pressed[i] = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.world.EXIT = True
                elif event.key == pygame.K_DELETE:
                    self.delete = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP0:
                    self.keypad_0 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP1:
                    self.keypad_1 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP2:
                    self.keypad_2 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP3:
                    self.keypad_3 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP4:
                    self.keypad_4 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP5:
                    self.keypad_5 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP6:
                    self.keypad_6 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP7:
                    self.keypad_7 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP8:
                    self.keypad_8 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP9:
                    self.keypad_9 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_0:
                    self.k_0 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_1:
                    self.k_1 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_2:
                    self.k_2 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_3:
                    self.k_3 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_LEFT:
                    self.k_left = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RIGHT:
                    self.k_right = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_DOWN:
                    self.k_down = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_UP:
                    self.k_up = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_a:
                    self.k_a = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_d:
                    self.k_d = event.type == pygame.KEYDOWN

        self.mouse_pos = pygame.mouse.get_pos()

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
    def __init__(self, world):
        super(GameState, self).__init__(world)
        self.n_players = 0

    def handleInput(self):
        super(GameState, self).handleInput()
        if (self.k_1):
            self.k_1 = False
            return self.world.GAMESTATE.reverse_mapping[0]
        elif(self.keypad_0):
            self.keypad_0 = False
            playership.PlayerShip(self)
        elif(self.keypad_1):
            self.keypad_1 = False
            label.Label(self, "Test", 49, util.TERM_BLUE, [50, 50])
        return self.world.GAMESTATE.reverse_mapping[1]

    def fixedUpdate(self):
        super(GameState, self).fixedUpdate()

    def update(self, delta):
        super(GameState, self).update(delta)

    def render(self):
        super(GameState, self).render()

class MenuState(WorldState):
    def __init__(self, world):
        super(MenuState, self).__init__(world)

        self.setupMenu()

    def setupMenu(self):
        label.Label(self, "MENU", 60, util.TERM_BLUE,
                            [self.world.WIDTH / 2, 30])

        button.PlayButton(self, "Play", 35, util.WHITE,
                            [self.world.WIDTH / 2, 300])

        button.Button(self, "Settings", 35, util.WHITE,
                            [self.world.WIDTH / 2, 350])

        button.Button(self, "Exit", 35, util.WHITE,
                            [self.world.WIDTH / 2, 400])

    def handleInput(self):
        super(MenuState, self).handleInput()
        if (self.k_2):
            self.k_2 = False
            return self.world.GAMESTATE.reverse_mapping[1]
        return self.world.GAMESTATE.reverse_mapping[0]

    def fixedUpdate(self):
        super(MenuState, self).fixedUpdate()

    def update(self, delta):
        super(MenuState, self).update(delta)

    def render(self):
        super(MenuState, self).render()
