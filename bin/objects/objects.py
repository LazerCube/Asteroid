import pygame
import settings
from utilites import util


class Objects(object):
    def __init__(self, world):
        self.worldstate = world
        self.name = None
        self.position = [0, 0]
        self.velocity = [0, 0]
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

    def updateHitBox(self):
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
            for i in range(3):
                if(self.mouseover and self.worldstate.mouse_pressed[i]):
                    self.mouse_active_press[i] = True
                else:
                    self.mouse_active_press[i] = False

    def fixedUpdate(self):
        if(self.mouse_active_press[0]):
            if(self.worldstate.delete):
                self.kill = True
        if self.kill:
            self.worldstate.remove(self)

        self.updateHitBox()


    def update(self, delta):
        pass

    def Draw(self):
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

    def fixedUpdate(self):
        self.log_data = self.worldstate.world.DEBUG_INFO + ("World Objects: %s  |  Sprites: %s  |  GUI: %s" %(self.worldstate.n_objects, self.worldstate.n_sprite, self.worldstate.N_GUIobjects))
        self.log = ("%s:     %s" %(self.log_name, self.log_data))
        self.rendered_text = self.text_info.render(self.log, True, (255,255,255))
        super(Debug, self).fixedUpdate()

    def update(self, delta):
        pass

    def Draw(self):
        pygame.draw.rect(self.worldstate.world.SURFACE, self.background_colour,
                        (settings.DEBUG_CONSOLE_X, settings.DEBUG_CONSOLE_Y, settings.DEBUG_CONSOLE_WIDTH, settings.DEBUG_CONSOLE_HEIGHT))
        #self.worldstate.world.SURFACE.blit(self.text, self.text_position)
        self.worldstate.world.SURFACE.blit(self.rendered_text, self.text_position)



class Sprite(Objects):
    def __init__(self, world):
        super(Sprite, self).__init__(world)
        self.worldstate.n_sprite += 1
        self.points = []
        self.screen_points = []

        self.max_velocity = 45
        self.rotate = 0

    def rotate_by(self, angle):
        self.angle += angle
        self.angle %=360

    def handleInput(self):
        super(Sprite, self).handleInput()
        if self.hover:
            if(self.mouseover):
                self.color = util.TERM_BLUE
                self.velocity = [0, 0]
                if(self.mouse_active_press[0]):
                    self.position = self.worldstate.mouse_pos
            else:
                self.color = util.WHITE

    def fixedUpdate(self):
        if self.kill:
            self.worldstate.n_sprite -= 1

        super(Sprite, self).fixedUpdate()

        self.rotate_by(self.rotate)

        for i in range(2):
            if (self.velocity[i] > self.max_velocity):
                self.velocity[i] = self.max_velocity
            elif (self.velocity[i] < -self.max_velocity):
                self.velocity[i] = - self.max_velocity


        self.position = [self.position[0] + (self.velocity[0]),
                         self.position[1] + (self.velocity[1])]

        self.position[0] %= self.worldstate.world.WIDTH
        self.position[1] %= self.worldstate.world.HEIGHT
        self.updateHitBox()

    def update(self, delta):
        interp_position = self.position
        interp_velocity = self.velocity

        interp_angle = self.angle
        interp_rotate = self.rotate

        view_position = [interp_position[0] + (interp_velocity[0]  * delta),
                         interp_position[1] + (interp_velocity[1]) * delta]

        view_angle = interp_angle + (interp_rotate * delta)

        a = self.scale * util.cos(view_angle)
        b = self.scale * -util.sin(view_angle)
        c = -b
        d = a

        self.screen_points = [[int(a * x + b * y + view_position[0]),
                              int(c * x + d * y + view_position[1])]
                              for x, y in self.points]

        super(Sprite, self).update(delta)

    def Draw(self):
        pygame.draw.lines(self.worldstate.world.SURFACE,
                          self.color, True, self.screen_points)

        super(Sprite, self).Draw()


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

        self.updateHitBox()

    def updateHitBox(self):
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

        super(GUI, self).updateHitBox()

    def handleInput(self):
        super(GUI, self).handleInput()


    def fixedUpdate(self):
        if self.kill:
            self.worldstate.N_GUIobjects -= 1
        super(GUI, self).fixedUpdate()

        if self.hover:
            if(self.mouseover):
                self.addtext(self.text, self.fontsize, util.RED)
                if(self.mouse_active_press[0]):
                    self.position = self.worldstate.mouse_pos
            else:
                self.addtext(self.text, self.fontsize, self.color)

    def update(self, delta):
        pass

    def Draw(self):
        super(GUI, self).Draw()
        self.worldstate.world.SURFACE.blit(self.GUI, self.new_position)
