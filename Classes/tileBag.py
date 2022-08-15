import pygame
from .tile import Tile
from .constants import *
import random


class TileBag:
    def __init__(self):
        self.default_tileset = TILE_BAG_COUNTS
        self._tiles_in_bag = self._fill_bag()

    def get_tile_count(self) -> int:
        return len(self._tiles_in_bag)

    def _fill_bag(self) -> [Tile]:
        tiles = []
        for letter in self.default_tileset:
            for _ in range(self.default_tileset[letter]):
                tiles.append(Tile(letter))
        return tiles

    def get_tiles(self, count) -> [Tile]:
        if len(self._tiles_in_bag):
            starting_tiles_in_bag = len(self._tiles_in_bag)
            tiles = [self._tiles_in_bag.pop(random.randrange(0, len(self._tiles_in_bag))) for _ in
                     range(min(count, len(self._tiles_in_bag)))]

            if count > starting_tiles_in_bag:
                need = count - starting_tiles_in_bag
                tiles.extend([Tile() for _ in range(need)])

            return tiles
        else:
            return [Tile() for _ in range(count)]



