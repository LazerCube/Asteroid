import pygame
import settings
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
        self.hitbox_pos = [0,0]
        self.kill = False
        self.scale = 10
        self.angle = 0
        self.color = util.WHITE
        self.mouseover = False              #   is the mouse over the object?
        self.mouse_active_press = [False] * 3
        self.hover = False                 #   Can the object be hovered?

        self.worldstate.add(self)

    def UpdateHitBox(self):
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        self.hitbox_pos = [[int(a * x + b * y + self.position[0]),
                            int(c * x + d * y + self.position[1])]
                           for x, y in self.hitbox]

    def HandleInput(self):
        if self.hover:
            if self.worldstate.mouse_pos[0] >= self.hitbox_pos[0][0] and self.worldstate.mouse_pos[1] >= self.hitbox_pos[0][1]:
                if self.worldstate.mouse_pos[0] <= self.hitbox_pos[3][0] and self.worldstate.mouse_pos[1] <= self.hitbox_pos[3][1]:
                    self.mouseover = True
                else:
                    self.mouseover = False
            else:
                self.mouseover = False
            for i in range(3):
                if(self.mouseover and self.worldstate.mouse_pressed[i]):
                    self.mouse_active_press[i] = True
                else:
                    self.mouse_active_press[i] = False

    def Update(self):
        if self.kill:
            print("Kill")
            self.worldstate.remove(self)
        if(self.mouse_active_press[0]):
            if(self.worldstate.delete):
                self.kill = True

    def Draw(self, delta):
        if self.worldstate.DEBUG_MODE:
            pygame.draw.lines(self.worldstate.world.SURFACE,
                              util.GREEN, True, self.hitbox_pos)
            for i in xrange(0, (len(self.hitbox_pos)), 2):
                if(i == 0):
                    pygame.draw.circle(self.worldstate.world.SURFACE, util.RED,
                                       (self.hitbox_pos[i]), 5, 0)
                else:
                    pygame.draw.circle(self.worldstate.world.SURFACE, util.GREEN,
                                       (self.hitbox_pos[i]), 5, 0)

class Debug(Objects):
    def __init__(self, world):
        super(Debug, self).__init__(world)
        self.n_DEBUG_objects = 0

        self.background_colour = settings.DEBUG_CONSOLE_BACKGROUND_COLOR

        self.font = util.DEFAULT_FONT
        self.text_position = ((settings.DEBUG_CONSOLE_X + 10),(settings.DEBUG_CONSOLE_Y + 10))
        self.text_info = pygame.font.SysFont(self.font, 18)
        self.log_name = "Debug log"
        self.rendered_text = self.text_info.render(self.log_name, True, (255,255,255))

    def Update(self):
        self.log_data = self.worldstate.world.DEBUG_INFO + ("World Objects: %s  |  Sprites: %s  |  GUI: %s" %(self.worldstate.n_objects, self.worldstate.n_sprite, self.worldstate.N_GUIobjects))
        self.log = ("%s:     %s" %(self.log_name, self.log_data))
        self.rendered_text = self.text_info.render(self.log, True, (255,255,255))
        super(Debug, self).Update()

    def Draw(self, delta):
        pygame.draw.rect(self.worldstate.world.SURFACE, self.background_colour,
                        (settings.DEBUG_CONSOLE_X, settings.DEBUG_CONSOLE_Y, settings.DEBUG_CONSOLE_WIDTH, settings.DEBUG_CONSOLE_HEIGHT))
        #self.worldstate.world.SURFACE.blit(self.text, self.text_position)
        self.worldstate.world.SURFACE.blit(self.rendered_text, self.text_position)



class Sprite(Objects):
    def __init__(self, world):
        super(Sprite, self).__init__(world)
        self.worldstate.n_sprite += 1
        self.velocity = [0, 0]
        self.points = []

    def HandleInput(self):
        super(Sprite, self).HandleInput()
        if self.hover:
            if(self.mouseover):
                self.color = util.TERM_BLUE
                self.velocity = [0, 0]
                if(self.mouse_active_press[0]):
                    self.position = self.worldstate.mouse_pos
                    self.UpdateHitBox()
            else:
                self.color = util.WHITE

    def Update(self):
        if self.kill:
            self.worldstate.n_sprite -= 1

        self.position = [self.position[0] + (self.velocity[0]),
                         self.position[1] + (self.velocity[1])]

        self.position[0] %= self.worldstate.world.WIDTH
        self.position[1] %= self.worldstate.world.HEIGHT
        self.UpdateHitBox()

    def Draw(self, delta):
        self.view_position = [self.position[0] + (self.velocity[0] * delta),
                              self.position[1] + (self.velocity[1] * delta)]

        super(Sprite, self).Draw(delta)
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        screen_points = [[int(a * x + b * y + self.view_position[0]),
                          int(c * x + d * y + self.view_position[1])]
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
        self.fontsize = fontsize
        self.color = color
        self.GUIinfo = None
        self.GUI = None

        self.debug_info = "gui object"

        self.addtext(self.text, self.fontsize, self.color)
        self.worldstate.N_GUIobjects += 1

    def addtext(self, text, fontsize, color):
        self.GUIinfo = pygame.font.SysFont(self.font, fontsize)
        self.GUI = self.GUIinfo.render(text, True, color)

        self.GUI_size = [(self.GUI.get_width()), (self.GUI.get_height())]
        self.GUI_center = [((self.GUI_size[0])/2), ((self.GUI_size[1])/2)]

        self.UpdateHitBox()

    def UpdateHitBox(self):
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

        super(GUI, self).UpdateHitBox()

    def HandleInput(self):
        super(GUI, self).HandleInput()
        if self.hover:
            if(self.mouseover):
                self.addtext(self.text, self.fontsize, util.RED)
                if(self.mouse_active_press[0]):
                    self.position = self.worldstate.mouse_pos
                    self.UpdateHitBox()
            else:
                self.addtext(self.text, self.fontsize, self.color)

    def Update(self):
        if self.kill:
            self.worldstate.N_GUIobjects -= 1
        super(GUI, self).Update()

    def Draw(self, delta):
        #self.screen_position = [self.new_position[0] * delta, self.new_position[1] * delta]
        super(GUI, self).Draw(delta)
        self.worldstate.world.SURFACE.blit(self.GUI, self.new_position)
