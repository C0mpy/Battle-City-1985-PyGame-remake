# 1. installirati pygame 1.9.1 cp35 za python 3.5

import pygame
import os
import Board
import Tank

os.environ['SDL_VIDEO_CENTERED'] = '1'  # za centriranje prozora
pygame.init()

"""board za igru je dimenzija 14 x 14, jedan kvadratic je 25 x 25 px - dodatna mesta su ostavljena za informacije o igri
"""
screen = pygame.display.set_mode((768, 672))  # glavni prozor
screen.set_alpha(None)
pygame.display.set_caption("Battle City 2016")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

font = pygame.font.Font(None, 36)
text_normal = font.render("Normal  Mode", 1, (250, 250, 250))
textpos = text_normal.get_rect()
textpos.center = (background.get_rect().centerx, background.get_rect().centery - 20)
background.blit(text_normal, textpos)
text_hard = font.render("Hard  Mode", 1, (250, 250, 250))
textpos.center = (background.get_rect().centerx, background.get_rect().centery + 20)
background.blit(text_hard, textpos)
circle = pygame.draw.circle(background, (0, 150, 200), (background.get_rect().centerx - 95,
                                                        background.get_rect().centery - 20), 5, 0)
screen.blit(background, (0, 0))
pygame.display.flip()

mode = "Normal"
selected = False
while not selected:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill((0, 0, 0))

            font = pygame.font.Font(None, 36)
            text_normal = font.render("Normal  Mode", 1, (250, 250, 250))
            textpos = text_normal.get_rect()
            textpos.center = (background.get_rect().centerx, background.get_rect().centery - 20)
            background.blit(text_normal, textpos)
            text_hard = font.render("Hard  Mode", 1, (250, 250, 250))
            textpos.center = (background.get_rect().centerx, background.get_rect().centery + 20)
            background.blit(text_hard, textpos)

            if event.key == pygame.K_DOWN:
                mode = "Hard"
                circle = pygame.draw.circle(background, (0, 150, 200), (background.get_rect().centerx - 95,
                                                                        background.get_rect().centery + 20), 5, 0)
            elif event.key == pygame.K_UP:
                mode = "Normal"
                circle = pygame.draw.circle(background, (0, 150, 200), (background.get_rect().centerx - 95,
                                                                        background.get_rect().centery - 20), 5, 0)
            elif event.key == pygame.K_RETURN:
                selected = True

    screen.blit(background, (0, 0))
    pygame.display.flip()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
#  za sivi UI
pygame.draw.rect(background, (225, 225, 225), [0, 0, 768, 24])
pygame.draw.rect(background, (225, 225, 225), [672, 24, 768, 672])
pygame.draw.rect(background, (225, 225, 225), [0, 648, 768, 672])
pygame.draw.rect(background, (225, 225, 225), [0, 0, 48, 672])

#  init igre
board = Board.Board()
board.load_next_level()
board.all_sprites.clear(screen, background)
clock = pygame.time.Clock()  # da bi imali fps
frame = 1  # brojac frejmova, da bi stvorili tenkice u ordedjenom trenutku

while not board.level_end:

    #  event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:

            if not board.player.moved:
                if event.key == pygame.K_LEFT:
                    board.player.move_left()
                    board.player.moved = True
                elif event.key == pygame.K_RIGHT:
                    board.player.move_right()
                    board.player.moved = True
                elif event.key == pygame.K_UP:
                    board.player.move_up()
                    board.player.moved = True
                elif event.key == pygame.K_DOWN:
                    board.player.move_down()
                    board.player.moved = True
                elif event.key == pygame.K_ESCAPE:
                    quit()
            if event.key == pygame.K_SPACE:
                board.player.fire()
        else:
            if board.player.moved and event.type == pygame.KEYUP:
                if board.player.direction == "DOWN" and event.key == pygame.K_DOWN or \
                        board.player.direction == "UP" and event.key == pygame.K_UP:
                    board.player.stop_vertical_movement()
                elif board.player.direction == "RIGHT" and event.key == pygame.K_RIGHT or \
                        board.player.direction == "LEFT" and event.key == pygame.K_LEFT:
                    board.player.stop_horizontal_movement()

    #  update svih objekata na mapi
    board.all_sprites.update()
    rects = board.all_sprites.draw(screen)
    pygame.display.update(rects)

    #  za stvaranje tenkica
    for tank_to_spawn in board.tanks_to_spawn:  # prolazimo kroz listu tenkica koje treba stvoriti
        if tank_to_spawn[3] == frame:  # ako je frame na kome treba da se stvori odredjeni tenkic
            tank = Tank.Tank(tank_to_spawn[0], tank_to_spawn[1], tank_to_spawn[2], tank_to_spawn[4], mode)
            board.tanks_to_spawn.remove(tank_to_spawn)
            board.tanks_group.add(tank)
            board.all_sprites.add(tank)

    #  za odabir pozicije tenkicima
    if mode == "Hard":
        for i in board.tanks_group:
            i.choose_direction()
    elif mode == "Normal":
        for i in board.tanks_group:
            i.choose_direction_normal()

    #  kraj nivoa
    if not len(board.target.groups()):
        board.level_end = True
    if not len(board.tanks_group) and not len(board.tanks_to_spawn):
        board.level_end = True

    clock.tick(30)
    frame += 1
