from threading import Thread

import pygame

from game.actors.ActorArrow import ActorArrow
from game.actors.ActorPlayer import ActorPlayer
from game.actors.ActorRock import ActorRock
from game.actors.ActorWall import ActorWall
from game.utils.Register import Register


class Loader(Thread):

    def __init__(self):
        super().__init__()

        self.finish = False

    def run(self):
        # Loading stuff here

        ActorWall.register()
        ActorArrow.register()
        ActorPlayer.register()
        ActorRock.register()

        self.finish = True

