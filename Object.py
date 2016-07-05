import pygame


class Object(pygame.sprite.DirtySprite):

    def __init__(self, kind, x, y):

        pygame.sprite.DirtySprite.__init__(self)
        self.type = kind

        if kind == "1":
            self.image = pygame.image.load("imgs/brick1.png")
        elif kind == "2":
            self.image = pygame.image.load("imgs/brick2.png")
        elif kind == "S":
            self.image = pygame.image.load("imgs/stone.png")
        elif kind == "T":
            self.image = pygame.image.load("imgs/target.png")

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
