from classes.text_sprite import TextSprite
import pygame


class MinesCounter(TextSprite):
    def update(self):
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, self.width, self.height), 1, 10)
        self.set_text(f"mines: {self.board.flags_count}/{self.board.all_bombs_count}")
