from classes.text_sprite import TextSprite
import pygame


class RestartSprite(TextSprite):
    def update(self):
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, self.width, self.height), 1, 10)
        self.set_text("Click to restart")

    def left_click(self, mouse_x, mouse_y):
        mouse_x -= self.rect.x
        mouse_y -= self.rect.y
        if 0 < mouse_x < self.width and 0 < mouse_y < self.height:
            self.board.restart()
