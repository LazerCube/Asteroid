import pygame
from utilites import util

class Objects(object):
    def __init__(self, world):
        self.worldstate = world
        self.name = None
        self.position = [0, 0]
        self.hitbox = [[-1, -1], [-1, 1],
                       [-1, 1], [1, 1],
                       [1, 1], [1, -1],
                       [1, -1], [-1, -1]]
        self.hitbox_pos = []
        self.kill = False
        self.scale = 10
        self.angle = 0
        self.color = util.WHITE
        self.mouseover = False              #   is the mouse over the object?
        self.hover = False                 #   Can the object be hovered?

        self.worldstate.add(self)

    def updatehitbox(self):
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        self.hitbox_pos = [[int(a * x + b * y + self.position[0]),
                            int(c * x + d * y + self.position[1])]
                           for x, y in self.hitbox]

    def handleInput(self):
        if self.hover:
            if self.worldstate.mouse_pos[0] >= self.hitbox_pos[0][0] and self.worldstate.mouse_pos[1] >= self.hitbox_pos[0][1]:
                if self.worldstate.mouse_pos[0] <= self.hitbox_pos[3][0] and self.worldstate.mouse_pos[1] <= self.hitbox_pos[3][1]:
                    self.mouseover = True
                else:
                    self.mouseover = False
            else:
                self.mouseover = False

    def Update(self):
        pass

    def Draw(self):
        pygame.draw.lines(self.worldstate.world.SURFACE,
                          util.GREEN, True, self.hitbox_pos)
        for i in xrange(0, (len(self.hitbox_pos)), 2):
            if(i == 0):
                pygame.draw.circle(self.worldstate.world.SURFACE, util.RED,
                                   (self.hitbox_pos[i]), 5, 0)
            else:
                pygame.draw.circle(self.worldstate.world.SURFACE, util.GREEN,
                                   (self.hitbox_pos[i]), 5, 0)

class Sprite(Objects):
    def __init__(self, world):
        super(Sprite, self).__init__(world)
        world.n_sprite += 1
        self.velocity = [0, 0]
        self.points = []

    def handleInput(self):
        super(Sprite, self).handleInput()
        if(self.mouseover):
            self.color = util.TERM_BLUE
            self.velocity = [0, 0]
            if(self.worldstate.mouse_pressed[0]):
                self.position = self.worldstate.mouse_pos

                self.updatehitbox()
            else:
                self.velocity = [1, 1]
        else:
            self.color = util.WHITE
            self.velocity = [1, 1]

    def Update(self):
        super(Sprite, self).Update()
        self.position = [self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1]]

        self.position[0] %= self.worldstate.world.WIDTH
        self.position[1] %= self.worldstate.world.HEIGHT
        self.updatehitbox()

    def Draw(self):
        super(Sprite, self).Draw()
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        screen_points = [[int(a * x + b * y + self.position[0]),
                          int(c * x + d * y + self.position[1])]
                         for x, y in self.points]

        pygame.draw.lines(self.worldstate.world.SURFACE,
                          self.color, True, screen_points)


class GUI(Objects):
    def __init__(self, world, text, fontsize, color, position):
        super(GUI, self).__init__(world)
        self.scale = 1
        self.angle = 0
        self.text = text
        self.fontsize = fontsize
        self.font = util.DEFAULT_FONT
        self.GUI_size = [0, 0]
        self.GUI_center = [0, 0]
        self.position = position
        self.new_position = position
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.GUIinfo = None
        self.GUI = None

        self.debug_info = "gui object"

        self.addtext(self.text, self.fontsize, self.color)
        world.N_GUIobjects += 1

    def addtext(self, text, fontsize, color):
        self.GUIinfo = pygame.font.SysFont(self.font, fontsize)
        self.GUI = self.GUIinfo.render(text, True, color)

        self.GUI_size = [(self.GUI.get_width()), (self.GUI.get_height())]
        self.GUI_center = [((self.GUI_size[0])/2), ((self.GUI_size[1])/2)]

        self.updatehitbox()

    def updatehitbox(self):
        self.new_position = [int(self.position[0] - self.GUI_center[0]),
                             int(self.position[1] - self.GUI_center[1])]

        a = [int(-self.GUI_center[0]), (-self.GUI_center[1])]
        b = [int(self.GUI_center[0]), (-self.GUI_center[1])]
        c = [int(self.GUI_center[0]), (self.GUI_center[1])]
        d = [int(-self.GUI_center[0]), (self.GUI_center[1])]

        self.hitbox[0] = a
        self.hitbox[1] = b
        self.hitbox[2] = b
        self.hitbox[3] = c
        self.hitbox[4] = c
        self.hitbox[5] = d
        self.hitbox[6] = d
        self.hitbox[7] = a

        super(GUI, self).updatehitbox()

    def handleInput(self):
        super(GUI, self).handleInput()
        if self.hover:
            if(self.mouseover):
                self.addtext(self.text, self.fontsize, util.RED)
                if(self.worldstate.mouse_pressed[0]):
                    self.position = self.worldstate.mouse_pos
                    self.updatehitbox()
            else:
                self.addtext(self.text, self.fontsize, self.color)

    def Update(self):
        super(GUI, self).Update()

    def Draw(self):
        super(GUI, self).Draw()
        self.worldstate.world.SURFACE.blit(self.GUI, self.new_position)
