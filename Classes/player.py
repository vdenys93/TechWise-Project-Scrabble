import pygame
from .tile import Tile


"""
Author:Team 4
Program:player.py
Player class
"""
class Player:
    PLAYER_NUM = (1, 2, 3, 4)

    # create a list of player nicknames and player scores to be used for scoreboard display
    nickname_list = []
    score_list = []

    """Player class"""
    def __init__(self, nick_name, player_num, turn_count=0, turn_since_last_placement=0, score=0):
        name_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'- 1234567890")
        if not (name_characters.issuperset(nick_name)):
            raise ValueError
        if player_num not in self.PLAYER_NUM:
            raise ValueError
        if not isinstance(turn_count, int):
            raise ValueError
        if not isinstance(turn_since_last_placement, int):
            raise ValueError
        if not isinstance(score, int):
            raise ValueError
        self.nick_name = nick_name
        self.player_num = player_num
        self.turn_count = turn_count
        self.turn_since_last_placement = turn_since_last_placement
        self.tile_array = []
        self.last_placed_word = [] # (x,y) tuples of location on board
        self.skip_next_turn = False
        Player.nickname_list.append(nick_name) # Add nickname to the nickname display list for scoreboard
        Player.score_list.append(score) # Add score to score display list for scoreboard
        self.score = score

    def tile_count(self) -> int:
        non_null_tiles = 0
        for t in self.tile_array:
            if t.is_tile():
                non_null_tiles += 1
        return non_null_tiles

    # Update the score list for the scoreboard
    def update_score_list(self):
        index = 1
        while index <= len(Player.score_list):
            if index == self.player_num:
                Player.score_list[index - 1] = self.score
            index += 1
