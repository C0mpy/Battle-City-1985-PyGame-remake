import pygame
import Bullet
from random import shuffle


class Tank(pygame.sprite.DirtySprite):

    def __init__(self, kind, x, y, board, mode):

        pygame.sprite.DirtySprite.__init__(self)
        self.x = x  # x koordinata tenkica
        self.y = y  # y koordinata tenkica
        self.x_change = 0  # vrednost za koju u svakom frejmu menjamo x osu tenkica
        self.y_change = 0  # vrednost za koju u svakom frejmu menjamo y osu tenkica
        self.type = kind  # tip tenkica
        self.can_fire = True  # da li tenkic moze da puca u ovom frejmu
        self.rate_of_fire = 0  # pomocna promenljiva za pucanje
        self.dirty = 2  # potrebno za DirtySprite, 2 znaci da se iscrtava ponovo u svakom frejmu
        self.bullet_group = pygame.sprite.RenderPlain()  # grupa metkica za ovaj tenkic
        self.board = board
        self.mode = mode  # mode igre, od njega zavisi i ponasanje tenkica
        self.directions = 0 #

        if kind == "PLAYER":
            self.image = pygame.image.load("imgs/player_lvl1.png")
            self.direction = "UP"  # smer kretanja
            self.moved = False  # pomocna promenljiva da ne bi moglo da se ide u koso (levo i gore u isto vreme npr)
            self.tanks_group = self.board.tanks_group

        elif kind == "ENEMY_LVL1":
            self.image = pygame.image.load("imgs/enemy_lvl1.png")
            self.direction = "DOWN"
            self.moved = False
            self.tanks_group = self.board.player_group

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move_left(self):

        self.x_change = -5
        if self.direction == "UP":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "RIGHT":
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.image, 270)
        self.direction = "LEFT"

    def move_right(self):

        self.x_change = 5
        if self.direction == "UP":
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.image, 90)
        self.direction = "RIGHT"

    def move_up(self):

        self.y_change = -5
        if self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == "RIGHT":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.image, 180)
        self.direction = "UP"

    def move_down(self):

        self.y_change = 5
        if self.direction == "UP":
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == "RIGHT":
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.image, 90)
        self.direction = "DOWN"

    def stop_vertical_movement(self):

        self.moved = False
        self.y_change = 0

    def stop_horizontal_movement(self):

        self.moved = False
        self.x_change = 0

    def fire(self):

        if self.can_fire:
            b = None
            if self.direction == "UP":
                b = Bullet.Bullet("UP", self.x, self.y - 10, self.board.destructable_objects,
                                  self.board.indestructable_objects, self.tanks_group)
                self.bullet_group.add(b)
            elif self.direction == "DOWN":
                b = Bullet.Bullet("DOWN", self.x, self.y + 10, self.board.destructable_objects,
                                  self.board.indestructable_objects, self.tanks_group)
                self.bullet_group.add(b)
            elif self.direction == "LEFT":
                b = Bullet.Bullet("LEFT", self.x - 10, self.y, self.board.destructable_objects,
                                  self.board.indestructable_objects, self.tanks_group)
                self.bullet_group.add(b)
            elif self.direction == "RIGHT":
                b = Bullet.Bullet("RIGHT", self.x + 10, self.y, self.board.destructable_objects,
                                  self.board.indestructable_objects, self.tanks_group)
                self.bullet_group.add(b)
            self.board.all_sprites.add(b)
            self.can_fire = False

    def update(self):

        self.x += self.x_change
        self.y += self.y_change
        self.rect.center = (self.x, self.y)

        # podesavanje pucanja
        self.rate_of_fire += 1
        if self.rate_of_fire // 15 == 1:
            self.rate_of_fire = 1
            self.can_fire = True

        # da ne bi moglo da se prolazi kroz objekte
        if (self.x < 66) or (self.x > 653) or\
                (self.y < 42) or (self.y > 629):
            self.revert_movement()
            return
        else:
            collision = pygame.sprite.spritecollide(self, self.board.destructable_objects, False)  # kolizija tenkica sa objektima
            if len(collision) != 0:
                self.revert_movement()
                return
            else:
                collision1 = pygame.sprite.spritecollide(self, self.board.indestructable_objects, False)  # -||-
                if len(collision1) != 0:
                    self.revert_movement()
                    return

    def revert_movement(self):

        if self.direction == "UP" or self.direction == "DOWN":
            self.y -= self.y_change
        else:
            self.x -= self.x_change
        self.rect.center = (self.x, self.y)

    def choose_direction(self):

        #  pucaj na igraca ako se nalazi direktno ispred tebe
        pos = {"UP": (0, -5), "DOWN": (0, 5), "LEFT": (-5, 0), "RIGHT": (5, 0)}
        if self.can_fire:
            if self.target_player(pos[self.direction]):
                self.fire()
            pos.pop(self.direction)
            #  okreni se ka igracu ako se nalazi levo desno ili ispod tebe
            for key in pos.keys():
                if self.target_player(pos[key]):
                    if key == "UP":
                        self.move_up()
                    elif key == "DOWN":
                        self.move_down()
                    elif key == "LEFT":
                        self.move_left()
                    elif key == "RIGHT":
                        self.move_right()
                    return

        #  izaberi smer kretanja za tenkic
        min_index = -1
        min_value = 100000000

        positions = [[self.x+8, self.y, "RIGHT", False], [self.x-8, self.y, "LEFT", False],
                     [self.x, self.y+8, "DOWN", False], [self.x, self.y-8, "UP", False]]

        good = []
        for i in positions:  # izbaciti nevalidne pozicije(izlaze van mape ili stone block)
            if 67 < i[0] < 657 and 634 > i[1] > 38:
                self.rect.center = (i[0], i[1])
                collision = pygame.sprite.spritecollide(self, self.board.indestructable_objects, False)
                if len(collision) == 0:
                    good.append(i)

        for i in list(range(len(good))):  # od preostalih validnih pozicija odaberi najbolju (vodi ka target)

            self.rect.center = (good[i][0], good[i][1])
            collision = pygame.sprite.spritecollide(self, self.board.destructable_objects, False)
            val = (self.board.target_x - good[i][0]) ** 2 + (self.board.target_y - good[i][1]) ** 2
            if len(collision) != 0:
                if val > 10000:
                    val *= 2
                good[i][3] = True
            if val < min_value:
                min_value = val
                min_index = i

        # ako je kretanje kroz ciglu onda pucaj, u suprotnom kreni u odredjenom smeru
        if good[min_index][3] and self.direction == good[min_index][2]:
            self.fire()
            return
        elif good[min_index][2] == "UP":
            self.x_change = 0
            self.move_up()
        elif good[min_index][2] == "DOWN":
            self.x_change = 0
            self.move_down()
        elif good[min_index][2] == "LEFT":
            self.y_change = 0
            self.move_left()
        elif good[min_index][2] == "RIGHT":
            self.y_change = 0
            self.move_right()
        self.rect.center = (good[min_index][0], good[min_index][1])

    def target_player(self, direction):

        temp_x = self.x
        temp_y = self.y
        while True:
            if 69 < temp_x < 654 and 631 > temp_y > 45:
                temp_x += direction[0] * 9
                temp_y += direction[1] * 9
                self.rect.center = (temp_x, temp_y)
                collision_destructable = pygame.sprite.spritecollide(self, self.board.destructable_objects, False)
                collision_indestructable = pygame.sprite.spritecollide(self, self.board.indestructable_objects, False)
                if len(collision_destructable) != 0 or len(collision_indestructable) != 0:
                    return False
                collision_tanks = pygame.sprite.spritecollide(self, self.tanks_group, False)
                if len(collision_tanks) != 0:
                    return True
            else:
                return False

    def choose_direction_normal(self):

        #  pucaj na igraca ako se nalazi direktno ispred tebe
        pos = {"UP": (0, -5), "DOWN": (0, 5), "LEFT": (-5, 0), "RIGHT": (5, 0)}
        if self.can_fire:
            if self.target_player(pos[self.direction]):
                self.fire()

        if (self.board.target_x - self.x) ** 2 <= 40000 and (self.board.target_y - self.y) ** 2 <= 40000:
            self.choose_direction()
            return
        # izaberi smer kretanja za tenkic
        positions = [[self.x + 10, self.y, "RIGHT", False], [self.x - 10, self.y, "LEFT", False],
                     [self.x, self.y + 10, "DOWN", False], [self.x, self.y - 10, "UP", False]]

        good = []
        for i in positions:  # izbaciti nevalidne pozicije(izlaze van mape ili stone block)
            if 69 < i[0] < 654 and 631 > i[1] > 45:
                self.rect.center = (i[0], i[1])
                collision = pygame.sprite.spritecollide(self, self.board.indestructable_objects, False)
                if len(collision) == 0:
                    collision1 = pygame.sprite.spritecollide(self, self.board.destructable_objects, False)
                    if len(collision1) == 0:
                        good.append(i)

        to_delete = ""
        if self.direction == "UP":
            to_delete = "DOWN"
        elif self.direction == "DOWN":
            to_delete = "UP"
        elif self.direction == "RIGHT":
            to_delete = "LEFT"
        elif self.direction == "LEFT":
            to_delete = "RIGHT"

        if len(good) != 1:
            for pos in good:
                if pos[2] == to_delete:
                    good.remove(pos)

        shuffle(good)
        if self.directions >= len(good):
            if good[0][2] == "UP":
                self.x_change = 0
                self.move_up()
            elif good[0][2] == "DOWN":
                self.x_change = 0
                self.move_down()
            elif good[0][2] == "LEFT":
                self.y_change = 0
                self.move_left()
            elif good[0][2] == "RIGHT":
                self.y_change = 0
                self.move_right()
            self.rect.center = (good[0][0], good[0][1])

        self.directions = len(good)