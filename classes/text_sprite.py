import pygame


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, board):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.font = pygame.font.SysFont('Verdana', 30)
        self.center = (width/2, height/2)

    def set_text(self, text):
        text_surface = self.font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.center)
        self.image.blit(text_surface, text_rect)

    def update(self):
        self.image.fill((0, 0, 0))
        if self.board.is_game_over:
            self.set_text("GAME OVER")
        elif self.board.is_game_won:
            self.set_text("WIN")
        else:
            self.set_text(f"mines: {self.board.flags_count}/{self.board.all_bombs_count}")
