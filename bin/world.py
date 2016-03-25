import pygame


from utilites import util
from objects import objects
from objects.sprite import playership


class WorldState(object):
    def __init__(self, world):
        self.world = world
        self.entities = []
        self.n_entities = 0
        self.n_sprite = 0
        self.N_GUIobjects = 0

        # objects
        self.sprite = objects.Sprite
        self.guiobjects = objects.GUI

        # Events
        self.resize = False

        # Keyboard Inputs
        self.escape = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.k_a = False
        self.k_d = False

        # Mouse Inputs
        self.mouse_pressed = [False, False, False]
        self.mouse_pos = [0, 0]

    def add(self, entitie):
        self.n_entities += 1
        self.entities.append(entitie)

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

        self.mouse_pos = pygame.mouse.get_pos()

        for i in self.entities:
            i.handleInput()

    def update(self):
        self.handleInput()
        for i in self.entities:
            i.Update()

    def render(self):
        for i in self.entities:
            i.Draw()

class GameState(WorldState):
    def __init__(self, world):
        super(GameState, self).__init__(world)
        self.n_players = 0

    def handleInput(self):
        super(GameState, self).handleInput()
        if (self.left):
            self.left = False
            return self.world.GAMESTATE.reverse_mapping[0]
        elif(self.down):
            self.down = False
            playership.PlayerShip(self)
        elif(self.up):
            self.up = False
            self.guiobjects(self, "Test", 49, util.TERM_BLUE, [50, 50]) # LOOK AT ONCE THE NEW STRUCTURE IS WORKING!!!
        return self.world.GAMESTATE.reverse_mapping[1]

    def update(self):
        super(GameState, self).update()
        util.BLACK = (120, 120, 120)

    def render(self):
        super(GameState, self).render()

class MenuState(WorldState):
    def __init__(self, world):
        super(MenuState, self).__init__(world)
        self.guiobjects(self, "MENU", 60, util.TERM_BLUE,
                            [self.world.WIDTH / 2, 30])

    def handleInput(self):
        super(MenuState, self).handleInput()
        if (self.right):
            self.right = False
            return self.world.GAMESTATE.reverse_mapping[1]
        return self.world.GAMESTATE.reverse_mapping[0]

    def update(self):
        super(MenuState, self).update()
        util.BLACK = (0, 0, 0)

    def render(self):
        super(MenuState, self).render()
