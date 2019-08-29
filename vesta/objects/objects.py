import pygame
import math

from vesta.config import settings
from vesta.utilites import util

class Objects(object):
    def __init__(self, world):
        self.worldstate = world
        self.GameEngine = world.GameEngine

        self.name = None
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.hitbox = [[-1, -1], [1, -1],
                       [1, -1], [1, 1],
                       [1, 1], [-1, 1],
                       [-1, 1], [-1, -1]]
        self.hitbox_pos = [0,0]
        self.alive = True
        self.scale = 10
        self.angle = 0
        self.color = settings.WHITE
        self.mouseover = False              #   is the mouse over the object?
        self.mouse_active_press = [False] * 3
        self.hover = False                 #   Can the object be hovered?

        self.worldstate.add(self)

    def update_hit_box(self):
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        self.hitbox_pos = [[int(a * x + b * y + self.position[0]),
                            int(c * x + d * y + self.position[1])]
                           for x, y in self.hitbox]

    def handle_input(self):
        if self.hover:
            if self.GameEngine.mouse_pos[0] >= self.hitbox_pos[0][0] and self.GameEngine.mouse_pos[1] >= self.hitbox_pos[0][1]:
                if self.GameEngine.mouse_pos[0] <= self.hitbox_pos[3][0] and self.GameEngine.mouse_pos[1] <= self.hitbox_pos[3][1]:
                    self.mouseover = True
                else:
                    self.mouseover = False
            else:
                self.mouseover = False
            for i in range(3):
                if(self.mouseover and self.GameEngine.mouse_pressed[i]):
                    self.mouse_active_press[i] = True
                else:
                    self.mouse_active_press[i] = False

    def fixed_update(self):
        if(self.mouse_active_press[0]):
            if(self.GameEngine.delete):
                self.kill()

        self.update_hit_box()


    def update(self, delta):
        pass

    def draw(self):
        if self.worldstate.DEBUG_MODE:
            pygame.draw.lines(self.GameEngine.Surface.SURFACE,
                              settings.GREEN, True, self.hitbox_pos)
            for i in xrange(0, (len(self.hitbox_pos)), 2):
                if(i == 0):
                    pygame.draw.circle(self.GameEngine.Surface.SURFACE, settings.RED,
                                       (self.hitbox_pos[i]), 5, 0)
                else:
                    pygame.draw.circle(self.GameEngine.Surface.SURFACE, settings.GREEN,
                                       (self.hitbox_pos[i]), 5, 0)
                        
    def kill(self):
        if self.alive:
            self.alive = False
            self.worldstate.remove(self)

class Debug(Objects):
    def __init__(self, world):
        super(Debug, self).__init__(world)
        self.worldstate.n_debug_objects += 1

        self.background_colour = settings.DEBUG_CONSOLE_BACKGROUND_COLOR

        self.font = settings.DEFAULT_FONT
        self.text_position = ((settings.DEBUG_CONSOLE_X + 10),(settings.DEBUG_CONSOLE_Y + 10))
        self.text_info = pygame.font.SysFont(self.font, 18)
        self.log_name = "Debug log"
        self.rendered_text = self.text_info.render(self.log_name, True, (255,255,255))

    def fixed_update(self):
        self.log_data = self.GameEngine.DEBUG_INFO + ("World Objects: %s  |  Sprites: %s  |  GUI: %s" %(self.worldstate.n_objects, self.worldstate.n_sprite, self.worldstate.n_gui_objects))
        self.log = ("%s:     %s" %(self.log_name, self.log_data))
        self.rendered_text = self.text_info.render(self.log, True, (255,255,255))
        super(Debug, self).fixed_update()

    def update(self, delta):
        pass

    def draw(self):
        pygame.draw.rect(self.GameEngine.Surface.SURFACE, self.background_colour,
                        (settings.DEBUG_CONSOLE_X, settings.DEBUG_CONSOLE_Y, settings.DEBUG_CONSOLE_WIDTH, settings.DEBUG_CONSOLE_HEIGHT))
        #self.worldstate.world.SURFACE.blit(self.text, self.text_position)
        self.GameEngine.Surface.SURFACE.blit(self.rendered_text, self.text_position)

    def kill(self):
        self.worldstate.n_debug_objects -= 1
        super(Sprite ,self).kill()

class Sprite(Objects):
    def __init__(self, world):
        super(Sprite, self).__init__(world)
        self.worldstate.n_sprite += 1
        self.points = []
        self.screen_points = []
        self.tested_collision = False

        self.max_velocity = 45
        self.angular_velocity = 0

        self.hover = False

        self.collision = True

        self.update_hit_box()

    def rotate_by(self, angle):
        self.angle += angle
        self.angle %=360

    def handle_input(self):
        super(Sprite, self).handle_input()
        if self.hover:
            if(self.mouseover):
                self.color = settings.TERM_BLUE
                self.velocity = [0, 0]
                if(self.mouse_active_press[0]):
                    self.position = self.GameEngine.mouse_pos
            else:
                self.color = settings.WHITE

    def update_collision_map(self):
        self.tested_collision = False

        map_x = int(self.position[0] / self.worldstate.COLLISION_MAP_RESOLUTION)
        map_y = int(self.position[1] / self.worldstate.COLLISION_MAP_RESOLUTION)

        # Tells collision map what squares this object is occupying
        for a in range(map_x - 1, map_x + 2):
            for b in range(map_y - 1, map_y + 2):
                current_map_cell = self.worldstate.collision_map[a % self.worldstate.COLLISION_MAP_WIDTH][b % self.worldstate.COLLISION_MAP_HEIGHT]
                if not current_map_cell == []:
                    self.test_collisions(current_map_cell)
                current_map_cell.append(self)

    def fixed_update(self):
        super(Sprite, self).fixed_update()

        self.rotate_by(self.angular_velocity)

        for i in range(2):
            if (self.velocity[i] > self.max_velocity):
                self.velocity[i] = self.max_velocity
            elif (self.velocity[i] < -self.max_velocity):
                self.velocity[i] = - self.max_velocity


        self.position = [self.position[0] + (self.velocity[0]),
                         self.position[1] + (self.velocity[1])]

        self.position[0] %= self.GameEngine.Surface.WIDTH
        self.position[1] %= self.GameEngine.Surface.HEIGHT

        self.update_hit_box()
        self.update_collision_map()

    def update(self, delta):
        interp_position = self.position
        interp_velocity = self.velocity

        interp_angle = self.angle
        interp_rotate = self.angular_velocity

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

    def test_collisions(self, possible_sprites):
        width = self.GameEngine.Surface.WIDTH
        height = self.GameEngine.Surface.HEIGHT

        for other in possible_sprites:
            # if other == self:
            #     continue
            # if other.tested_collision:
            #     continue

            if other.alive:
                dx = self.position[0] - other.position[0]
                dy = self.position[1] - other.position[1]

                if dx > width / 2:
                    dx -= width
                elif dx < -width / 2:
                    dx += width

                if dy > height / 2:
                    dy -= height
                elif dy < -height / 2:
                    dy += height

                d2 = dx * dx + dy * dy 
                t = self.scale + other.scale
                t2 = t * t
                if d2 > t2:
                    continue
                
                d = math.sqrt(d2)
                if d == 0:
                    d = 0.0001
                u = dx / d
                v = dy / d

                overlap = d - t

                other.position[0] += u * overlap 
                other.position[0] %= width
                other.position[1] += v * overlap
                other.position[1] %= height

                self.impact(other)
                other.impact(self)

                if self.alive:
                    self.collide(other)

                self.tested_collision = True

    def collide(self, other):
        if self.collision:
            if other.collision:
                x = other.velocity[0]
                other.velocity[0] = self.velocity[0]
                self.velocity[0] = x

                y = other.velocity[1]
                other.velocity[1] = self.velocity[1]
                self.velocity[1] = y

    def impact(self, other):
        pass

    def kill(self):
        self.worldstate.n_sprite -= 1
        super(Sprite ,self).kill()

    def draw(self):
        pygame.draw.lines(self.GameEngine.Surface.SURFACE,
                          self.color, True, self.screen_points)

        super(Sprite, self).draw()


class GUI(Objects):
    def __init__(self, world, text, fontsize, color, position):
        super(GUI, self).__init__(world)
        self.scale = 1
        self.angle = 0
        self.text = text
        self.fontsize = fontsize
        self.font = settings.DEFAULT_FONT
        self.GUI_size = [0, 0]
        self.GUI_center = [0, 0]
        self.position = position
        self.new_position = position
        self.fontsize = fontsize
        self.color = color
        self.GUIinfo = None
        self.GUI = None

        self.debug_info = "gui object"

        self.add_text(self.text, self.fontsize, self.color)
        self.worldstate.n_gui_objects += 1

        self.update_hit_box()

    def add_text(self, text, fontsize, color):
        self.GUIinfo = pygame.font.SysFont(self.font, fontsize)
        self.GUI = self.GUIinfo.render(text, True, color)

        self.GUI_size = [(self.GUI.get_width()), (self.GUI.get_height())]
        self.GUI_center = [((self.GUI_size[0])/2), ((self.GUI_size[1])/2)]

        self.update_hit_box()

    def update_hit_box(self):
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

        super(GUI, self).update_hit_box()

    def handle_input(self):
        super(GUI, self).handle_input()


    def fixed_update(self):
        super(GUI, self).fixed_update()

        if self.hover:
            if(self.mouseover):
                self.add_text(self.text, self.fontsize, settings.RED)
            else:
                self.add_text(self.text, self.fontsize, self.color)

    def update(self, delta):
        pass

    def kill(self):
        self.worldstate.n_gui_objects -= 1
        super(GUI ,self).kill()

    def draw(self):
        super(GUI, self).draw()
        self.GameEngine.Surface.SURFACE.blit(self.GUI, self.new_position)

class ParticleSystem(Objects):
    def __init__(self, world, color, position):
        super(ParticleSystem, self).__init__(world)

        self.name = None
        self.position = position
        self.velocity = None
        self.hitbox = None
        self.hitbox_pos = None
        self.scale = 1
        self.color = color

        self.show_particles = True

        self.particles = {}
        self.particle_index = 0
    
    def update_hit_box(self):
        pass

    def handle_input(self):
        pass

    def show(self, show_particles):
        self.show_particles = show_particles

    def add(self, velocity, life):
        if not self.show_particles:
            return

        particle = [life,
                     self.position[0], self.position[1], 
                    velocity[0], velocity[1]]
        self.particles[self.particle_index] = particle
        self.particle_index += 1

    def n_particles(self):
        return len(self.particles)

    def remove_all(self):
        self.particles = {}

    def fixed_update(self):
        if not self.show_particles:
            return

        keys = self.particles.keys()
        if keys:
            for i in keys:
                part = self.particles[i]
                if part[0] > 0:
                    part[0] -= 1
                    if part[0] == 0:
                        del self.particles[i]
                        continue

                    part[1] += part[3]
                    part[2] += part[4]
                    
                    part[1] %= self.GameEngine.Surface.WIDTH
                    part[2] %= self.GameEngine.Surface.HEIGHT
        else:
            self.kill()

    def draw(self):
        if not self.show_particles:
            return

        for i in self.particles:
            part = self.particles[i]
            rect = [part[1], part[2], 3, 3]
            pygame.draw.rect(self.GameEngine.Surface.SURFACE, self.color, rect)
                        
    def kill(self):
        if self.alive:
            self.alive = False
            self.worldstate.remove(self)