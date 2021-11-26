import os

import pygame
from math import sqrt
import random
import numpy as np
from classes.hexagon import Hexagon


class Board(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.center = (width/2, height/2)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.font = pygame.font.SysFont('Verdana', 30)

        self.icon_size = (40, 40)
        filepath = os.path.dirname(__file__)
        flag_icon = pygame.image.load(os.path.join(filepath, '..', 'images', 'flag_icon.png'))
        bomb_icon = pygame.image.load(os.path.join(filepath, '..', 'images', 'bomb_icon.png'))
        self.flag_icon = pygame.transform.scale(flag_icon, self.icon_size)
        self.bomb_icon = pygame.transform.scale(bomb_icon, self.icon_size)

        self.d = 2.5
        self.a = 30
        self.b = self.a-2 * self.d

        self.rows = 10
        self.cols = 12
        self.hexes_count = self.rows * self.cols
        self.all_bombs_count = 10
        self.not_bombs_count = self.hexes_count-self.all_bombs_count

        self.hexagons_width = sqrt(3) * self.a * (self.cols+0.5)
        self.hexagons_height = 1.5 * self.a * (self.rows+0.5)
        self.hexagons_corner = pygame.Vector2((self.width-self.hexagons_width) / 2,
                                              (self.height-self.hexagons_height) / 2)

        self.original_points_out = np.array([pygame.Vector2(0, -1 * self.a),
                                             pygame.Vector2(0.5 * sqrt(3) * self.a, -0.5 * self.a),
                                             pygame.Vector2(0.5 * sqrt(3) * self.a, 0.5 * self.a),
                                             pygame.Vector2(0, self.a),
                                             pygame.Vector2(-0.5 * sqrt(3) * self.a, 0.5 * self.a),
                                             pygame.Vector2(-0.5 * sqrt(3) * self.a, -0.5 * self.a)])
        self.original_points_in = np.array([pygame.Vector2(0, -1 * self.b),
                                            pygame.Vector2(0.5 * sqrt(3) * self.b, -0.5 * self.b),
                                            pygame.Vector2(0.5 * sqrt(3) * self.b, 0.5 * self.b),
                                            pygame.Vector2(0, self.b),
                                            pygame.Vector2(-0.5 * sqrt(3) * self.b, 0.5 * self.b),
                                            pygame.Vector2(-0.5 * sqrt(3) * self.b, -0.5 * self.b)])

        self.original_points_in += self.hexagons_corner
        self.original_points_out += self.hexagons_corner
        # for i in range(6):
        #    self.original_points_in[i] += self.hexagons_corner
        #    self.original_points_out[i] += self.hexagons_corner

        self.hexagons = np.array([Hexagon(self, index // self.cols, index % self.cols)
                                  for index in range(self.hexes_count)])
        self.is_first_checked = False
        self.is_game_over = False
        self.is_game_won = False
        self.flags_count = 0
        self.checked_count = 0

    def set_level(self, level):
        if level == 1:
            self.set_settings(8, 6, 8)
        elif level == 2:
            self.set_settings(10, 8, 15)
        elif level == 3:
            self.set_settings(12, 10, 20)

    def set_settings(self, cols, rows, bombs):
        self.image.fill((0, 0, 0))
        self.rows = rows
        self.cols = cols
        self.hexes_count = self.rows * self.cols
        self.all_bombs_count = bombs
        self.not_bombs_count = self.hexes_count-self.all_bombs_count
        self.hexes_count = self.rows * self.cols
        self.hexagons_width = sqrt(3) * self.a * (self.cols+0.5)
        self.hexagons_height = 1.5 * self.a * (self.rows+0.5)
        self.hexagons_corner = pygame.Vector2((self.width-self.hexagons_width) / 2,
                                              (self.height-self.hexagons_height) / 2)

        self.original_points_out = np.array([pygame.Vector2(0, -1 * self.a),
                                             pygame.Vector2(0.5 * sqrt(3) * self.a, -0.5 * self.a),
                                             pygame.Vector2(0.5 * sqrt(3) * self.a, 0.5 * self.a),
                                             pygame.Vector2(0, self.a),
                                             pygame.Vector2(-0.5 * sqrt(3) * self.a, 0.5 * self.a),
                                             pygame.Vector2(-0.5 * sqrt(3) * self.a, -0.5 * self.a)])
        self.original_points_in = np.array([pygame.Vector2(0, -1 * self.b),
                                            pygame.Vector2(0.5 * sqrt(3) * self.b, -0.5 * self.b),
                                            pygame.Vector2(0.5 * sqrt(3) * self.b, 0.5 * self.b),
                                            pygame.Vector2(0, self.b),
                                            pygame.Vector2(-0.5 * sqrt(3) * self.b, 0.5 * self.b),
                                            pygame.Vector2(-0.5 * sqrt(3) * self.b, -0.5 * self.b)])

        self.original_points_in += self.hexagons_corner
        self.original_points_out += self.hexagons_corner

        self.hexagons = np.array([Hexagon(self, index // self.cols, index % self.cols)
                                  for index in range(self.hexes_count)])
        self.is_first_checked = False
        self.is_game_over = False
        self.restart()

    def left_click(self, mouse_x, mouse_y):
        hexagon = self.find_hexagon(mouse_x-0, mouse_y-0)
        if hexagon is not None:
            hexagon.check()

    def right_click(self, mouse_x, mouse_y):
        hexagon = self.find_hexagon(mouse_x-0, mouse_y-0)
        if hexagon is not None:
            hexagon.set_flag()

    def restart(self):
        self.is_first_checked = False
        self.is_game_over = False
        self.is_game_won = False
        self.flags_count = 0
        self.checked_count = 0
        for hexagon in self.hexagons:
            hexagon.is_checked = False
            hexagon.is_flagged = False
            hexagon.is_bomb = False

    def set_bombs(self, index):
        # setting bombs
        bomb_hexagons = random.sample(set(range(0, self.hexes_count))-{index}, self.all_bombs_count)
        for i in bomb_hexagons:
            self.hexagons[i].is_bomb = True

        # counting neighbors and bombs
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols+j
                neighbors_count = 0
                bombs_count = 0
                if i % 2 == 0:
                    all_coordinates = [(i-1, j-1), (i-1, j), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j)]
                else:
                    all_coordinates = [(i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j), (i+1, j+1)]
                for coordinates in all_coordinates:
                    if 0 <= coordinates[0] < self.rows and 0 <= coordinates[1] < self.cols:
                        neighbor_index = coordinates[0] * self.cols+coordinates[1]
                        self.hexagons[index].neighbors.append(self.hexagons[neighbor_index])
                        neighbors_count += 1
                        if self.hexagons[neighbor_index].is_bomb:
                            bombs_count += 1
                self.hexagons[index].set_neighbors_count(neighbors_count, bombs_count)

    def update(self):
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, self.width, self.height), 1, 10)
        for hexagon in self.hexagons:
            hexagon.draw()
        # self.rect = self.surf.get_rect()
        if self.is_game_over:
            self.draw_alert("GAME OVER")
        elif self.is_game_won:
            self.draw_alert("YOU WIN")

    def find_hexagon(self, mouse_x, mouse_y):

        mouse_x -= (self.hexagons_corner.x+self.rect.x)
        mouse_y -= (self.hexagons_corner.y+self.rect.y)

        # checking level_y
        level_y, y_in = divmod(mouse_y, 1.5 * self.a)
        if level_y < 0 or level_y > self.rows:
            return

        # checking level_x
        if level_y % 2 == 0:
            level_x, x_in = divmod(mouse_x, sqrt(3) * self.a)
        else:
            level_x, x_in = divmod(mouse_x-0.5 * sqrt(3) * self.a, sqrt(3) * self.a)

        # checking left corner of the rectangle
        if y_in < -sqrt(3) / 3 * x_in+0.5 * self.a:
            if level_y % 2 == 0:
                level_x -= 1
                level_y -= 1
            else:
                level_y -= 1

        # checking left corner of the rectangle
        if y_in < sqrt(3) / 3 * x_in-0.5 * self.a:
            if level_y % 2 == 0:
                level_y -= 1
            else:
                level_x += 1
                level_y -= 1

        if level_x < 0 or level_x >= self.cols or level_y < 0 or level_y >= self.rows:
            return

        level_x = int(level_x)
        level_y = int(level_y)
        return self.hexagons[level_y * self.cols+level_x]

    def draw_alert(self, text):
        pygame.draw.rect(self.image, (0, 0, 0), (self.width/2 - 100, self.height/2 - 20, 200, 40), 0, 10)
        pygame.draw.rect(self.image, (255, 0, 0), (self.width / 2-100, self.height / 2-20, 200, 40), 1, 10)
        text_surface = self.font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.center)
        self.image.blit(text_surface, text_rect)
