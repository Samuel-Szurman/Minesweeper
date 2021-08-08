from classes.text_sprite import TextSprite


class StatusSprite(TextSprite):
    def update(self):
        self.image.fill((0, 0, 0))
        if self.board.is_game_over:
            self.set_text("GAME OVER")
        elif self.board.is_game_won:
            self.set_text("YOU WIN")
