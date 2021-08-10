import pygame
from math import sqrt


class Hexagon:
    black = (0, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    orange = (255, 165, 0)
    gray = (165, 165, 165)

    def __init__(self, board, row, col):
        self.board = board
        self.row = row
        self.col = col

        self.is_bomb = False
        self.is_checked = False
        self.is_flagged = False

        self.neighbors = []
        self.neighbors_count = 0
        self.bombs_count = 0

        if row % 2 == 0:
            x = 0.5 * sqrt(3) * self.board.a + col * (self.board.a * sqrt(3))
        else:
            x = self.board.a * sqrt(3) + col * self.board.a * sqrt(3)
        y = self.board.a + row * 1.5 * self.board.a

        self.current_color = self.blue
        self.points_out = self.board.original_points_out + (x, y)
        self.points_in = self.board.original_points_in + (x, y)

    def set_neighbors_count(self, neighbors_count, bombs_count):
        self.neighbors_count = neighbors_count
        self.bombs_count = bombs_count

    def draw(self):
        self.draw_colored_hex()
        self.draw_text()

    def draw_colored_hex(self):
        if self.is_checked:
            if self.is_bomb:
                self.current_color = Hexagon.red
            else:
                self.current_color = Hexagon.gray
        else:
            if self.is_flagged:
                pass
            else:
                self.current_color = Hexagon.white

        pygame.draw.polygon(self.board.image, self.current_color, self.points_in)

    def draw_text(self):
        if self.is_flagged:
            icon_pos = (self.points_in[0] + self.points_in[3] - pygame.Vector2(self.board.icon_size)) / 2
            self.board.image.blit(self.board.flag_icon, icon_pos)
        if self.is_checked:
            if self.is_bomb:
                icon_pos = (self.points_in[0]+self.points_in[3]-pygame.Vector2(self.board.icon_size)) / 2
                self.board.image.blit(self.board.bomb_icon, icon_pos)
            else:
                if self.bombs_count != 0:
                    self.set_text(str(self.bombs_count))

    def set_text(self, text):
        text_surface = self.board.font.render(text, False, Hexagon.black)
        text_rect = text_surface.get_rect(center=((self.points_out[2]+self.points_out[5]) / 2))
        self.board.image.blit(text_surface, text_rect)

    def change_state(self):
        if self.current_color == self.blue:
            self.current_color = self.green
        else:
            self.current_color = self.blue

    def set_flag(self):
        if not self.is_checked and not self.board.is_game_over and not self.board.is_game_won:
            self.is_flagged = not self.is_flagged
            if self.is_flagged:
                self.board.flags_count += 1
            else:
                self.board.flags_count -= 1

    def check(self, is_cascade=False):
        if not self.board.is_game_over and not self.board.is_game_won:
            if (not self.is_flagged or is_cascade) and not self.is_checked:
                if not self.board.is_first_checked:
                    self.board.is_first_checked = True
                    index = self.row*self.board.cols + self.col
                    self.board.set_bombs(index)
                self.is_checked = True
                if self.is_bomb:
                    self.board.is_game_over = True
                else:
                    self.board.checked_count += 1
                    if self.board.checked_count == self.board.not_bombs_count:
                        self.board.is_game_won = True
                if is_cascade:
                    self.is_flagged = False
                if not self.is_bomb and self.bombs_count == 0:
                    for neighbor in self.neighbors:
                        neighbor.check(is_cascade=True)
