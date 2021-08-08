from classes.board import Board
from classes.mines_counter import MinesCounter
from classes.status_sprite import StatusSprite
from classes.restart_sprite import RestartSprite
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

board = Board(50, 100, 700, 500)
status_sprite = StatusSprite(125, 5, 550, 40, board)
mines_counter = MinesCounter(125, 55, 250, 40, board)
restart_sprite = RestartSprite(425, 55, 250, 40, board)
sprites = pygame.sprite.Group()
sprites.add(board, status_sprite, mines_counter, restart_sprite)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                x, y = pygame.mouse.get_pos()
                board.left_click(x, y)
                restart_sprite.left_click(x, y)
            elif event.button == RIGHT:
                x, y = pygame.mouse.get_pos()
                board.right_click(x, y)

    screen.fill((0, 0, 0))
    sprites.update()
    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
