import pygame

from api.ActorAnimation import ActorAnimation
from api.Animation import Animation
from api.Timer import Timer
from game.actors.ActorArrow import ActorArrow
from game.actors.ActorCollidable import ActorCollidable
from game.utils.Direction import DIRECTION
from game.utils.SurfaceHelper import load_image
from game.utils.Vector import Vector, VECTOR_NULL
from game.utils.Constants import *


class ActorPlayer(ActorAnimation):
    ID = 3
    NAME = "PLAYER"

    def __init__(self):
        super().__init__()

        # On charge toutes les images etc...
        # Chargement des animations :
        # => ça a changé cf load_sprite()

        self.z = -50

        self.should_update = True
        self.handle_event = True

        self.direction = DIRECTION.BAS

        # Déplacements
        self.walk = False
        self.has_moved = False
        self.speed = 4  # En pixel par tick
        self.direction_walk = []

        self.velocity = Vector(0, 0)
        self.velocity_max = 4

        # Tirs
        self.shoot_rate = 200.0  # Nombre de tirs par second
        self.can_shoot = True
        self.is_shooting = False  # Pour l'animation ?
        self.shoot = False


        self.reload(None)


    def reload(self, map):
        super().reload(map)

        # Gestion des touches utilisés :
        # [key]: [activate?, direction(optional)] => toujours utilisé ce format

        self.keys_shoot = {
            273: [False, DIRECTION.HAUT],
            276: [False, DIRECTION.GAUCHE],
            274: [False, DIRECTION.BAS],
            275: [False, DIRECTION.DROITE]
        }

        self.keys_move = {
            122: [False, DIRECTION.HAUT],
            113: [False, DIRECTION.GAUCHE],
            115: [False, DIRECTION.BAS],
            100: [False, DIRECTION.DROITE]
        }

        self.keys_other = {

        }

        self.keys = [self.keys_shoot, self.keys_move, self.keys_other]
        self.direction = DIRECTION.BAS

    def unload(self):
        super().unload()

        del self.keys_shoot
        del self.keys_move
        del self.keys_other
        del self.keys
        del self.direction

    def load_sprite(self):
        sprites_sheet = load_image("assets/marinka.png", False)
        self.animations = {}

        self.animations[DIRECTION.HAUT] = Animation(sprites_sheet, pygame.Rect(PLAYER_MOVE_TOP.x * PLAYER_SPRITE_WIDTH,
                                                                               PLAYER_MOVE_TOP.y * PLAYER_SPRITE_HEIGHT,
                                                                               PLAYER_SPRITE_WIDTH,
                                                                               PLAYER_SPRITE_HEIGHT),
                                                    PLAYER_MOVE_TILES_NUMBER, PLAYER_MOVE_TIME, auto_rect=True)
        self.animations[DIRECTION.GAUCHE] = Animation(sprites_sheet,
                                                      pygame.Rect(PLAYER_MOVE_LEFT.x * PLAYER_SPRITE_WIDTH,
                                                                  PLAYER_MOVE_LEFT.y * \
                                                                  PLAYER_SPRITE_HEIGHT, PLAYER_SPRITE_WIDTH,
                                                                  PLAYER_SPRITE_HEIGHT),
                                                      PLAYER_MOVE_TILES_NUMBER, PLAYER_MOVE_TIME, True)
        self.animations[DIRECTION.DROITE] = Animation(sprites_sheet,
                                                      pygame.Rect(PLAYER_MOVE_RIGHT.x * PLAYER_SPRITE_WIDTH,
                                                                  PLAYER_MOVE_RIGHT.y * \
                                                                  PLAYER_SPRITE_HEIGHT, PLAYER_SPRITE_WIDTH,
                                                                  PLAYER_SPRITE_HEIGHT),
                                                      PLAYER_MOVE_TILES_NUMBER, PLAYER_MOVE_TIME, True)
        self.animations[DIRECTION.BAS] = Animation(sprites_sheet,
                                                   pygame.Rect(PLAYER_MOVE_BOTTOM.x * PLAYER_SPRITE_WIDTH,
                                                               PLAYER_MOVE_BOTTOM.y * \
                                                               PLAYER_SPRITE_HEIGHT, PLAYER_SPRITE_WIDTH,
                                                               PLAYER_SPRITE_HEIGHT),
                                                   PLAYER_MOVE_TILES_NUMBER, PLAYER_MOVE_TIME, True)
        self.animations[DIRECTION.NONE] = Animation(sprites_sheet, pygame.Rect(PLAYER_STANDBY.x * PLAYER_SPRITE_WIDTH,
                                                                               PLAYER_STANDBY.y * \
                                                                               PLAYER_SPRITE_HEIGHT,
                                                                               PLAYER_SPRITE_WIDTH,
                                                                               PLAYER_SPRITE_HEIGHT), 1, 1000, True)

        self.animation = self.animations[DIRECTION.NONE]

    def unload_sprite(self):
        super().unload_sprite()

        del self.animation
        del self.animations

        self.info("Sprites unloaded succesfuldzy!")

    def update(self):
        super().update()

        self.update_timers()

        self.walk = False
        self.direction = DIRECTION.NONE
        self.direction_walk = []
        for value in self.keys_move.values():
            if value[0] == True:
                self.direction = value[1]
                self.direction_walk.append(value[1])
                self.walk = True

        self.shoot = False
        for value in self.keys_shoot.values():
            if value[0] == True:
                self.direction = value[1]
                self.shoot = True
                break

        if self.walk:
            speed_x = 0
            speed_y = 0
            for dir in self.direction_walk:
                speed_x += dir.value.x
                speed_y += dir.value.y

            self.velocity.x = self.velocity_max * speed_x
            self.velocity.y = self.velocity_max * speed_y
        else:
            self.velocity.null()

        if self.velocity != VECTOR_NULL:
            self.has_moved = self.move(x=self.velocity.x, y=self.velocity.y)

        if self.has_moved == False:
            self.velocity.null()

        if self.shoot and self.can_shoot:
            self.is_shooting = True
            self.can_shoot = False
            self.add_timer(Timer(self.shoot_rate, self.turn_on_shoot))

            arrow = ActorArrow(self.direction, self.velocity)
            arrow.rect.x = self.rect.x + (self.rect.w - arrow.rect.w) / 2
            arrow.rect.y = self.rect.y + (self.rect.h - arrow.rect.w) / 2
            self.map.add_actor(arrow)

        self.animation = self.animations[self.direction]

    def move(self, x=0, y=0):  # Return True if the Player moved, False otherwise
        rect = pygame.Rect(self.rect)
        rect.x += x
        rect.y += y

        if self.map.is_at(rect, ActorCollidable) == -1:
            self.rect.x = rect.x
            self.rect.y = rect.y

            return True
        else:
            return False

    def turn_on_shoot(self, *args, **kwargs):
        self.can_shoot = True

    # Override methods

    def handle_keydown(self, unicode, key, mod):
        for index, keys in enumerate(self.keys):
            if key in keys.keys():
                self.keys[index][key][0] = True
                return True

    def handle_keyup(self, key, mod):
        for index, keys in enumerate(self.keys):
            if key in keys.keys():
                self.keys[index][key][0] = False
                return True
