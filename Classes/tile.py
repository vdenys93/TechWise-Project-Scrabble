import pygame
from .constants import *


class Tile:

    def __init__(self, character=""):
        self._letter = character
        self._points = TILE_SCORES[character]

    def get_points(self):
        return self._points

    def get_letter(self):
        return self._letter

    def set_letter(self, character):
        self._letter = character
        self._points = TILE_SCORES[character]

    def is_tile(self) -> bool:
        if self._letter == "":
            return False
        return True

    def draw(self, win, xcor: int, ycor: int):
        # mpos: tuple, win

        letter_font = pygame.font.Font('freesansbold.ttf', 16)
        letter_text = letter_font.render(self._letter, True, BLACK, None)
        letter_rect_obj = letter_text.get_rect()
        letter_rect_obj.center = ((SQUARE_SIZE // 2) + xcor, (SQUARE_SIZE // 2) + ycor)
        points_font = pygame.font.Font('freesansbold.ttf', 10)
        points_text = points_font.render(str(self._points), True, BLACK, None)
        points_rect_obj = points_text.get_rect()
        points_rect_obj.center = (SQUARE_SIZE - 8 + xcor, SQUARE_SIZE - 8 + ycor)  # 40 - 8
        tile_border_obj = pygame.Rect(xcor, ycor, SQUARE_SIZE - 1, SQUARE_SIZE - 1)
        pygame.draw.rect(win, WHITE, tile_border_obj)
        pygame.draw.rect(win, GREY, tile_border_obj, 1)
        win.blit(letter_text, letter_rect_obj)
        win.blit(points_text, points_rect_obj)
