from classes.board import Board
from classes.mines_counter import MinesCounter
from classes.return_sprite import ReturnSprite
from classes.restart_sprite import RestartSprite
from classes.level_sprite import LevelSprite
from classes.text_sprite import TextSprite
import pygame
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN
)

LEFT = 1
RIGHT = 3

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 30
clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Minesweeper')
icon = pygame.image.load('images/bomb_icon.png')
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('arial', 30)

# game sprites
board = Board(50, 50, 700, 500)
mines_counter = MinesCounter(300, 5, 200, 40, board)
return_sprite = ReturnSprite(150, 555, 250, 40, board)
restart_sprite = RestartSprite(450, 555, 250, 40, board)
game_sprites = pygame.sprite.Group()
game_sprites.add(board, mines_counter, return_sprite, restart_sprite)

# menu sprites
title_sprite = TextSprite(200, 100, 400, 50, "SELECT LEVEL")
level1_sprite = LevelSprite(300, 200, 200, 50, board, 1)
level2_sprite = LevelSprite(300, 280, 200, 50, board, 2)
level3_sprite = LevelSprite(300, 360, 200, 50, board, 3)
level_sprites = [level1_sprite, level2_sprite, level3_sprite]
menu_sprites = pygame.sprite.Group()
menu_sprites.add(title_sprite, level1_sprite, level2_sprite, level3_sprite)

is_menu_on = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                x, y = pygame.mouse.get_pos()
                if is_menu_on:
                    for level_sprite in level_sprites:
                        if level_sprite.is_clicked(x, y):
                            is_menu_on = False
                            break
                else:
                    board.left_click(x, y)
                    restart_sprite.left_click(x, y)
                    if return_sprite.is_clicked(x, y):
                        is_menu_on = True
            elif event.button == RIGHT:
                if not is_menu_on:
                    x, y = pygame.mouse.get_pos()
                    board.right_click(x, y)

    screen.fill((0, 0, 0))
    if is_menu_on:
        menu_sprites.update()
        menu_sprites.draw(screen)
    else:
        game_sprites.update()
        game_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
