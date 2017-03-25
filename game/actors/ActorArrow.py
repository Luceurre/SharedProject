import math

from api.ActorSprite import ActorSprite
from game.utils.Direction import DIRECTION
from game.utils.Vector import VECTOR_NULL, Vector


class ActorArrow(ActorSprite):

    ID = 2
    NAME = "ARROW"

    def __init__(self, dir=DIRECTION.NONE, velocity=VECTOR_NULL):
        super().__init__()
        self.damage = 5
        try:
            self.dir = dir.get_theta()
        except:
            self.dir = dir.value.get_theta()
        self.speed = 8
        self.velocity = Vector(0, 0)
        if math.cos(self.dir) * velocity.x >= 0:
            self.velocity.x = velocity.x / 2
        if math.sin(self.dir) * velocity.y >= 0:
            self.velocity.y = velocity.y / 2
        self.should_update = True

        self.draw_shadow = True
        self.collidable = True
        self.h = 20

    def reload(self):
        super().reload()

        self.draw_shadow = True
        self.h = 64
        self.collidable = True


    def update(self):
        super().update()

        # On essaye de bouger, si False est retourné, le projectile a rencontré un monstre, un mur, etc... et dans ce cas
        # on le détruit.
        if not self.move(self.speed * math.cos(self.dir) + self.velocity.x, self.speed * math.sin(self.dir) + self.velocity.y):
            self.map.remove_actor(self)
