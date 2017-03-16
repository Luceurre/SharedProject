import pygame

from game.utils.SurfaceHelper import get_real_rect


class Animation:
    def __init__(self, image, load_rect, tile_number, time=0, auto_rect=False, vertical=False):
        """Créer une animation à partir de 'image'. Chaque partie de l'Animation devra être contenu dans la zone 'load_rect'.
        Le nombre d'images dans l'animation est défini par 'tile_number' et le temps entre chaque image est 'time'.
        Finalement si les images doivent être automatiquement recadré 'auto_rect' doit être True et pour charger les images
        de haut en bas plutot que de gauche à droite 'vertical' doit également être égal à True.s"""


        self.tile = []
        self.rects = []
        self.auto_rect = auto_rect

        for i in range(tile_number):
            if not vertical:
                self.tile.append(
                    image.subsurface(load_rect.x + load_rect.width * i, load_rect.y, load_rect.width, load_rect.height))
            else:
                self.tile.append(
                    image.subsurface(load_rect.x, load_rect.y + load_rect.height * i, load_rect.width,
                                     load_rect.height))
        if auto_rect:
            # Obtention des hitboxs réels des images -> utils.Image.get_real_rect :
            rect = get_real_rect(self.tile[0])
            for index, tile in enumerate(self.tile):
                # On en profite pour redimensionner les images :
                self.tile[index] = tile.subsurface(rect)
                self.rects.append(rect)

        self.now = pygame.time.get_ticks()
        self.at = 0
        self.tile_number = tile_number
        self.time = time

    def next_sprite(self):
        """Renvoie l'image suivante dans l'Animation, si c'est la dernière image, renvoie None"""
        self.at += 1
        if self.at >= self.tile_number:
            return None
        else:
            return self.tile[self.at]

    def previous_sprite(self):
        """Renvoie l'image précèdente dans l'Animation, si c'est la première image, renvoie None"""
        self.at -= 1
        if self.at < 0:
            return None
        else:
            return self.tile[self.at]

    def get_sprite(self):
        if self.tile_number == 1 or self.time <= 0:
            return self.tile[0]
        elif pygame.time.get_ticks() - self.now >= self.time:
            self.at = (self.at + 1) % (self.tile_number - 1)
            self.now = pygame.time.get_ticks()

        return self.tile[self.at]

    def get_rect(self, rect):

        rect.size = self.rects[self.at].size
        return rect
