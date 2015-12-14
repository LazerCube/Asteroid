import pygame
import serversprite
import asteroid
import random
import socket

import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        #print data
        return
    def Close(self):
        print("CLOSE gameid %i" % self.gameid)
        self._server.close(self.gameid)
    def Network_other_player(self,data):
        pos = data["p"]
        angle = data["a"]
        num = data["num"]
        self.gameid = data["gameid"]
        self._server.other_player(pos, angle, data, self.gameid, num)


class GameServer(PodSixNet.Server.Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex=0

    def close(self,gameid):
        try:
            game = [a for a in self.games if a.gameid==gameid][0]
            game.player0.Send({"action":"close"})
            game.player1.Send({"action":"close"})
        except:
            pass

    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue==None:
            self.currentIndex+=1
            channel.gameid=self.currentIndex
            self.queue=Game(channel, self.currentIndex)
        else:
            channel.gameid=self.currentIndex
            self.queue.player1=channel
            self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            print("SERVER INFO: gameid: %i Game started!" % self.queue.gameid)
            self.queue=None

    def other_player(self, pos, angle, data, gameid, num):
        game =[a for a in self.games if a.gameid == gameid]
        if len(game)==1:
            game[0].other_player(pos, angle, data, num)


    def tick(self):
        for game in self.games:
            game.game_tick()
        self.Pump()


class Game(object):
    def __init__(self, player0, currentIndex):
        self.player0 = player0
        self.player1 = None
        self.gameid =  currentIndex
        self.width = 500
        self.height = 500

        self.sprites = []
        self.n_sprites = 0
        self.score = 0
        self.level = 1
        self.n_asteroids = 0

        asteroid.Asteroid(self, random.randint(50,100),1)

    def other_player(self, pos, angle, data, num):
        if num == 0:
            self.player1.Send({"action": "update", "p": pos, "a": angle})
        else:
            self.player0.Send({"action": "update", "p": pos, "a": angle})

    def game_tick(self):
        for i in self.sprites:
            i.update()
            #print(i.position)
            pos = i.position

            self.player1.Send({"action": "world", "p": pos})
            self.player0.Send({"action": "world", "p": pos})

    def add(self, serversprite):#creates a new instance of the class sprite
        self.sprites.append(serversprite)
        print(self.sprites)


print "STARTING SERVER ON LOCALHOST"
#try
pygame.init()
msPerTick = 15.625
lastTimer = pygame.time.get_ticks()
lastCurrentTime = pygame.time.get_ticks()

ticks = 0
delta = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Move into PodSixNet
s.connect(("8.8.8.8" , 80)) #Move into PodSixNet get_ip

address=raw_input("Host:Port (%s:8000): " %(s.getsockname()[0]))
if not address:
    host,port=(s.getsockname()[0]), 8000
    print("Using default IP and Port")
else:
    host,port = address.split(":")
gameServe = GameServer(localaddr = (host, int(port)))

print("SERVER START")

while True:
    currentTime = pygame.time.get_ticks()
    delta +=((currentTime - lastCurrentTime)/msPerTick)
    lastCurrentTime = currentTime


    while (delta >= 1):
        ticks += 1
        gameServe.tick()
        delta -= 1


    if(pygame.time.get_ticks() - lastTimer >= 1000):
        lastTimer += 1000
        #print("Server Ticks: %i " %(ticks))
        ticks = 0
