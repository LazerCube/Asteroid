from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import socket

import pygame
import util
import sprite
import player

class World(object, ConnectionListener):
    def __init__(self,surface):
        self.surface = surface
        self.font_info = pygame.font.SysFont(util.default_font, 16)
        self.font_hud = pygame.font.SysFont(util.default_font, 30)
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.sprites = []
        self.n_sprites = 0
        self.score = 0

        #Test Server side objects
        self.objectpos = 0
        self.objectpos2 = 0

        #Connection info
        self.gameid = None
        self.num = None
        self.host = None

        #inputs
        self.quit = False
        self.rotate_left = False
        self.rotate_right = False
        self.rotate_by = 0
        self.thrust = False
        self.info = False
        self.enter = False
        self.player = None
        self.other_player = None

        #Other Players
        self.other_player_position = [0,0]
        #self.other_player_velocity = [0,0]
        self.other_player_angle = 0

        self.server_setup()

    def server_setup(self):
        self.select_server()

        self.running=False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
        #determine attributes for player #
        if self.num==0:
            self.host = True
        else:
            self.host = False
        print("HOST CLIENT: %s " % self.host)

    def select_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Move into PodSixNet
        s.connect(("8.8.8.8" , 80)) #Move into PodSixNet get_ip

        address=raw_input("Address of Server(%s:8000): " %(s.getsockname()[0]))
        try:
            if not address:
                host, port=(s.getsockname()[0]) , 8000
                print("Using default IP and Port")
            else:
                host,port=address.split(":")
            self.Connect((host, int(port)))
        except:
            print "Error Connecting to Server"
            print "Usage:", "host:port"
            print "e.g.", "localhost:31425"
            exit()

        print "Game client started"

    def Network_close(self,data):
        print("DISCONNECT")
        self.quit = True

    def Network_startgame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameid=data["gameid"]
        print("CLIENT INFO: player: %i gameid: %i" % (self.num, self.gameid))

    def Network_update(self, data):
        self.other_player_position = data["p"]
        self.other_player_angle = data["a"]

    def Network_world(self,data):
        self.objectpos = [int(i) for i in (data["p"])]

    def add(self, sprite):#creates a new instance of the class sprite
        self.n_sprites += 1
        self.sprites.append(sprite)

    def add_player(self):# adds a player into the game
        if not self.player:
            self.player = player.player(self)
        if not self.other_player:
            self.other_player = player.player(self)

        if self.num ==0:
            self.other_player.team_color = util.TERM_BLUE
        else:
            self.player.team_color = util.TERM_BLUE


    def add_text(self, string, type):# handles rendering of text to screen. Takes text/type/location on screen
        if type == 'info':
            surface_font = self.font_info.render(string, True, util.RED)
            return surface_font
        elif type == 'hud':
            surface_font = self.font_hud.render(string, True, util.WHITE)
            return surface_font
        elif type == 'title':
            surface_font = self.font_title.render(string, True, util.WHITE)
            return surface_font
        elif type == 'gameover':
            surface_font = self.gameover.render(string, True, util.RED)
            return surface_font

    def update(self):
        connection.Pump()
        self.Pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode(event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

                self.width,self.height = (event.dict['size'])
                util.display_width, util.display_height = (event.dict['size'])

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_LEFT:
                    self.rotate_left = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RIGHT:
                     self.rotate_right = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_UP:
                    self.thrust = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_i:
                    if event.type == pygame.KEYDOWN:
                        if self.info == True:
                            self.info = False
                        else:
                            self.info = True
                elif event.key == pygame.K_RETURN:
                    self.enter = event.type == pygame.KEYDOWN

        if self.player:
            if self.rotate_left:
                self.rotate_by = -4
            elif self.rotate_right:
                self.rotate_by = 4
            else:
                self.rotate_by = 0
            if self.thrust:
                self.player.thrust()

            self.player.rotate_by(self.rotate_by)
            #self.Send({"action" : "other_player", "position":self.player.position, "velocity":self.player.velocity, "angle": self.player.angle,"gameid":self.gameid, "num":self.num})

            self.Send({"action" : "other_player", "p":self.player.position, "a":self.player.angle, "gameid":self.gameid, "num":self.num})

            self.other_player.position = self.other_player_position
            self.other_player.angle = self.other_player_angle


        for i in self.sprites:
            i.update()


    def draw(self):
        pygame.draw.circle(self.surface, util.RED, (self.objectpos),20, 0)
        for i in self.sprites:
            i.draw()
