from classes.text_sprite import TextSprite
import pygame


class StatusSprite(TextSprite):
    def __init__(self, pos_x, pos_y, width, height, board):
        TextSprite.__init__(self, pos_x, pos_y, width, height)
        self.board = board

    def update(self):
        if self.board.is_game_won or self.board.is_game_over:
            self.image.fill((0, 0, 0))
            pygame.draw.rect(self.image, (0, 0, 255), (0, 0, self.width, self.height), 1, 10)
        if self.board.is_game_over:
            self.set_text("GAME OVER")
        elif self.board.is_game_won:
            self.set_text("YOU WIN")
