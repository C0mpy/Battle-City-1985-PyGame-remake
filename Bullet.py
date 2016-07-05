import pygame


class Bullet(pygame.sprite.DirtySprite):

    def __init__(self, direction, x, y, objects, indestructable, tanks):

        pygame.sprite.DirtySprite.__init__(self)
        self.x = x
        self.y = y
        self.direction = direction
        self.image = pygame.image.load("imgs/bullet.png")

        if direction == "DOWN":
            self.image = pygame.transform.rotate(self.image, 180)
        elif direction == "RIGHT":
            self.image = pygame.transform.rotate(self.image, 270)
        elif direction == "LEFT":
            self.image = pygame.transform.rotate(self.image, 90)

        self.objects = objects
        self.indestructable = indestructable
        self.tanks = tanks

        self.rect = self.image.get_rect()
        self.dirty = 2

    def update(self):

        self.rect.center = (self.x, self.y)
        if self.direction == "UP":
            if self.y <= 35:
                self.kill()
                return
            self.y -= 10
        elif self.direction == "DOWN":
            if self.y >= 639:
                self.kill()
                return
            self.y += 10
        elif self.direction == "LEFT":
            if self.x <= 56:
                self.kill()
                return
            self.x -= 10
        elif self.direction == "RIGHT":
            if self.x >= 643:
                self.kill()
                return
            self.x += 10

        if len(pygame.sprite.spritecollide(self, self.objects, True)) != 0:
            self.kill()
            return
        else:
            if len(pygame.sprite.spritecollide(self, self.indestructable, False)) != 0:
                self.kill()
                return
            else:
                for tank in self.tanks:
                    if len(pygame.sprite.spritecollide(self, self.tanks, True)) != 0:
                        self.kill()
                        return
                    elif len(pygame.sprite.spritecollide(self, tank.bullet_group, True)) != 0:
                        self.kill()