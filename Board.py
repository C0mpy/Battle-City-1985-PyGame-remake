import pygame
import Tank
import Object


class Board:

    def __init__(self):

        self.current_level = 1
        self.player = None
        self.tanks_to_spawn = []
        self.target_x = 0
        self.target_y = 0
        self.level_end = False  # flag za kraj levela
        self.all_sprites = pygame.sprite.LayeredDirty()  # svi spriteovi se nalaze u ovoj grupi da bi ih update
        self.tanks_group = pygame.sprite.Group()  # protivnicki tenkici se nalaze u ovoj grupi da bi proveravao koliziju
        self.player_group = pygame.sprite.Group()  # tenkic igraca se nalazi u ovoj grupi da bi proveravao koliziju
        self.destructable_objects = pygame.sprite.Group()  # grupa objekata koji se mogu unistiti
        self.indestructable_objects = pygame.sprite.Group()  # grupa objekata koji se ne mogu unistiti

    def load_next_level(self):

        self.player = None
        self.tanks_to_spawn = []

        self.load_board()
        self.load_tanks()

        self.current_level += 1

    def load_board(self):

        with open("levels/board" + str(self.current_level) + ".txt") as myfile:
            data = myfile.readlines()
            for i in list(range(len(data))):
                for j in list(range(len(data[i]))):

                    if data[i][j] == "1" or data[i][j] == "2":

                        obj = Object.Object(data[i][j], 54 + 12 * j, 30 + 12 * i)
                        self.all_sprites.add(obj)
                        self.destructable_objects.add(obj)

                    elif data[i][j] == "S":

                        obj = Object.Object(data[i][j], 60 + 12 * j, 36 + 12 * i)
                        self.all_sprites.add(obj)
                        self.indestructable_objects.add(obj)

                    elif data[i][j] == "T":
                        self.target_x = 70 + 12 * j
                        self.target_y = 50 + 12 * i
                        obj = Object.Object(data[i][j], self.target_x, self.target_y)
                        obj.dirty = 2
                        self.all_sprites.add(obj)
                        self.destructable_objects.add(obj)
                        self.target = obj

    def load_tanks(self):

        with open("levels/tanks" + str(self.current_level) + ".txt") as myfile:
            for line in myfile:
                content = line.split("-")
                if content[0] == "PLAYER":
                    self.player = Tank.Tank("PLAYER", float(content[1]), float(content[2]), self, None)
                    self.player_group.add(self.player)
                    self.all_sprites.add(self.player)
                elif content[0] == "ENEMY_LVL1":

                    self.tanks_to_spawn.append([content[0], float(content[1]), float(content[2]), int(content[3]), self])