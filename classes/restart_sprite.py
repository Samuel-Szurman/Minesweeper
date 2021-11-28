from classes.text_sprite import TextSprite
import pygame


class RestartSprite(TextSprite):
    def __init__(self, pos_x, pos_y, width, height, board):
        TextSprite.__init__(self, pos_x, pos_y, width, height)
        self.board = board

    def update(self):
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, self.width, self.height), 1, 10)
        self.set_text("Click to restart")
