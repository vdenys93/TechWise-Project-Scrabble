# import pygame
import sys
import random
import time
from .board import Board
from .player import Player
from .tile import Tile
from .tileBag import TileBag
from .constants import *


class Controller:
    def __init__(self, win):
        self._board = Board()
        self._players = []
        self._tile_bag = TileBag()
        self._temp_tile = Tile()
        self._placed_tiles = []
        self.win = win
        self.current_players_turn = 0  # by index
        self.player_selection_is_complete = False
        self.clicked=False

    def place_tile(self, xy: tuple):
        self._placed_tiles.append(xy)

    def remove_tile(self, xy: tuple):
        self._placed_tiles.remove(xy)

    def draw_text(self, text, x, y):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(text, True, BLACK, BLUE)
        text_rect = text.get_rect()
        text_rect.center = (x // 2, y // 2)

    def create_players(self, number_of_players):
        #Create First Two Players
        self._players.append(Player("Player 1", 1))
        self._players.append(Player("Player 2", 2))

        #Add Additional Players
        if number_of_players == 3:
            self._players.append(Player("Player 3", 3))
        elif number_of_players == 4:
            self._players.append(Player("Player 3", 3))
            self._players.append(Player("Player 4", 4))

    def get_player_count(self, win, event):
        scrabble_font = pygame.font.Font('freesansbold.ttf', 32)
        font = pygame.font.Font('freesansbold.ttf', 24)
        #Text Display
        welcome_text = scrabble_font.render('Welcome to Scrabble!', True, BLACK)
        self.win.blit(welcome_text, (175, 75))
        how_many_players_text = font.render('Enter the Number of Players', True, BLACK)
        self.win.blit(how_many_players_text, (175, 180))

        #Two Person Selection Button
        two_player_button = pygame.Rect(BOARD_WIDTH // 2, SQUARE_SIZE * 7, SQUARE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, LT_GREY, two_player_button)
        pygame.draw.rect(self.win, GREY, two_player_button, 1)
        two_player_text = font.render('2', True, BLACK)
        two_text_rect = two_player_text.get_rect(center=(BOARD_WIDTH // 2 + (SQUARE_SIZE * 1.5), SQUARE_SIZE * 7 + (TILE_SIZE * .5)))
        self.win.blit(two_player_text, two_text_rect)

        #Three Person Selection Button
        three_player_button = pygame.Rect(BOARD_WIDTH // 2, SQUARE_SIZE * 11, SQUARE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, LT_GREY, three_player_button)
        pygame.draw.rect(self.win, GREY, three_player_button, 1)
        three_player_text = font.render('3', True, BLACK)
        three_text_rect = three_player_text.get_rect(center=(BOARD_WIDTH // 2 + (SQUARE_SIZE * 1.5), SQUARE_SIZE * 11 + (TILE_SIZE * .5)))
        self.win.blit(three_player_text, three_text_rect)

        #Four Person Selection Button
        four_player_button = pygame.Rect(BOARD_WIDTH // 2, SQUARE_SIZE * 15, SQUARE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, LT_GREY, four_player_button)
        pygame.draw.rect(self.win, GREY, four_player_button, 1)
        four_player_text = font.render('4', True, BLACK)
        four_text_rect = four_player_text.get_rect(center=(BOARD_WIDTH // 2 + (SQUARE_SIZE * 1.5), SQUARE_SIZE * 15 + (TILE_SIZE * .5)))
        self.win.blit(four_player_text, four_text_rect)

        #Create Players based on button selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if two_player_button.collidepoint(mpos[0], mpos[1]):
                self.create_players(2)
                self.player_selection_is_complete = True
            elif three_player_button.collidepoint(mpos[0], mpos[1]):
                self.create_players(3)
                self.player_selection_is_complete = True
            elif four_player_button.collidepoint(mpos[0], mpos[1]):
                self.create_players(4)
                self.player_selection_is_complete = True

    def pass_out_tiles(self):
        random.shuffle(self._tile_bag._tiles_in_bag)
        for player in self._players:
            if len(player.tile_array) == 0:
                player.tile_array = self._tile_bag.get_tiles(7)
            elif len(player.tile_array) < 7:
                count = 7 - len(player.tile_array)
                player.tile_array = player.tile_array + (self._tile_bag.get_tiles(count))

    def shuffle_tile_rack(self):
        for player in self._players:
            random.shuffle(player.tile_array)

    def start(self, win):
        # get_player_count(win)
        self.pass_out_tiles()

    def adjacent_word_points(self):
        score_total = 0
        for xy in self._placed_tiles:
            adjacent_letters = [(xy[0], xy[1] - 1),

                                (xy[0] - 1, xy[1]), (xy[0] + 1, xy[1]),

                                (xy[0], xy[1] + 1)
                                ]
            for idx, a in enumerate(adjacent_letters):
                if a not in self._placed_tiles \
                        and 0 < a[0] < 15 \
                        and 0 < a[1] < 15 \
                        and self._board._board[a[0]][a[1]].is_tile():
                    # north
                    direction = [0, 0]
                    if idx == 0:
                        direction = [0, -1]
                    # east
                    if idx == 1:
                        direction = [-1, 0]
                    # west
                    if idx == 2:
                        direction = [1, 0]
                    # south
                    if idx == 3:
                        direction = [0, 1]

                    xy = list(a)

                    while self._board._board[xy[0]][xy[1]].is_tile():
                        score_total += self._board._board[xy[0]][xy[1]].get_points()
                        xy[0] += direction[0]
                        xy[1] += direction[1]
        return score_total

    def calculate_points(self, game_board: Board):
        word_score, double_word_bonus, triple_word_bonus = 0, 0, 0
        adjacent_words = self.adjacent_word_points()
        # adjacent_words = 0
        for i in self._placed_tiles:
            letter_bonus = 0
            if BOARD_PATTERN[i[0]][i[1]] == 'TW':
                triple_word_bonus += 1
            elif BOARD_PATTERN[i[0]][i[1]] == 'DW':
                double_word_bonus += 1
            if BOARD_PATTERN[i[0]][i[1]] == 'TL':
                letter_bonus = 3
            elif BOARD_PATTERN[i[0]][i[1]] == 'DL':
                letter_bonus = 2
            if letter_bonus > 0:
                word_score += game_board._board[i[0]][i[1]].get_points() * letter_bonus
            else:
                word_score += game_board._board[i[0]][i[1]].get_points()
        if double_word_bonus > 0:
            for n in range(double_word_bonus):
                word_score += game_board._board[i[0]][i[1]].get_points() * 2
        if triple_word_bonus > 0:
            for n in range(triple_word_bonus):
                word_score += game_board._board[i[0]][i[1]].get_points() * 3
        return word_score + adjacent_words

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = int(y // SQUARE_SIZE)
        col = int(x // SQUARE_SIZE)
        return col, row

    def next_turn(self):
        self._placed_tiles = []
        self.pass_out_tiles()
        if self.current_players_turn == len(self._players) - 1:
            self.current_players_turn = 0
        else:
            self.current_players_turn += 1
        if self._players[self.current_players_turn].skip_next_turn == True:
            self.next_turn()

        pygame.display.flip()

    # Player turn display
    def player_turn_display(self, win):
        win.fill(LT_CYAN)
        # Set scoreboard dimensions
        scoreboard_object = pygame.Rect(SQUARE_SIZE, SQUARE_SIZE / 2, SCOREBOARD_WIDTH, SQUARE_SIZE)
        # Draw scoreboard background
        pygame.draw.rect(win, WHITE, scoreboard_object)

        #Highlight current players turn
        if len(self._players) == 2:
            player_one_highlighter= pygame.Rect(SQUARE_SIZE, SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 2, SQUARE_SIZE)
            player_two_highlighter = pygame.Rect(SQUARE_SIZE + SCOREBOARD_WIDTH / 2, SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 2, SQUARE_SIZE)
            if self.current_players_turn == 0:
                pygame.draw.rect(win, YELLOW, player_one_highlighter)
            else:
                pygame.draw.rect(win, YELLOW, player_two_highlighter)
            pygame.draw.rect(win, BLACK, player_one_highlighter, 1)
        elif len(self._players) == 3:
            player_one_highlighter = pygame.Rect(SQUARE_SIZE, SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 3, SQUARE_SIZE)
            player_two_highlighter = pygame.Rect(SQUARE_SIZE + (SCOREBOARD_WIDTH / 3) , SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 3, SQUARE_SIZE)
            player_three_highlighter = pygame.Rect(SQUARE_SIZE + (SCOREBOARD_WIDTH / 3 * 2) , SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 3, SQUARE_SIZE)
            if self.current_players_turn == 0:
                pygame.draw.rect(win, YELLOW, player_one_highlighter)
            elif self.current_players_turn == 1:
                pygame.draw.rect(win, YELLOW, player_two_highlighter)
            else:
                pygame.draw.rect(win, YELLOW, player_three_highlighter)
            pygame.draw.rect(win, BLACK, player_one_highlighter, 1)
            pygame.draw.rect(win, BLACK, player_two_highlighter, 1)
            pygame.draw.rect(win, BLACK, player_three_highlighter, 1)
        else:
            player_one_highlighter = pygame.Rect(SQUARE_SIZE, SQUARE_SIZE // 2, SCOREBOARD_WIDTH / 4, SQUARE_SIZE)
            player_two_highlighter = pygame.Rect(SQUARE_SIZE + (SCOREBOARD_WIDTH * .25), SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 4, SQUARE_SIZE)
            player_three_highlighter = pygame.Rect(SQUARE_SIZE + (SCOREBOARD_WIDTH * .5), SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 4, SQUARE_SIZE)
            player_four_highlighter = pygame.Rect(SQUARE_SIZE + (SCOREBOARD_WIDTH * .75), SQUARE_SIZE / 2, SCOREBOARD_WIDTH / 4, SQUARE_SIZE)

            if self.current_players_turn == 0:
                pygame.draw.rect(win, YELLOW, player_one_highlighter)
            elif self.current_players_turn == 1:
                pygame.draw.rect(win, YELLOW, player_two_highlighter)
            elif self.current_players_turn == 2:
                pygame.draw.rect(win, YELLOW, player_three_highlighter)
            else:
                pygame.draw.rect(win, YELLOW, player_four_highlighter)
            pygame.draw.rect(win, BLACK, player_one_highlighter, 1)
            pygame.draw.rect(win, BLACK, player_two_highlighter, 1)
            pygame.draw.rect(win, BLACK, player_three_highlighter, 1)
            pygame.draw.rect(win, BLACK, player_four_highlighter, 1)

        #Draw scoreboard border
        pygame.draw.rect(win, BLACK, scoreboard_object, 2)

    def tile_count_display(self):
        button_rect = pygame.Rect(4, SQUARE_SIZE * 4, TILE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, TAN, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 12)
        tile_count_display_button = font.render("Tile Count: " + str(self._tile_bag.get_tile_count()), True, BLACK)
        tile_count_display_button_rect = font.render("Tile Count: " + str(self._tile_bag.get_tile_count()), True, BLACK)
        tile_count_display_button_rect = tile_count_display_button.get_rect(center=(4 + (TILE_SIZE * 1.5), SQUARE_SIZE * 4.5))
        self.win.blit(tile_count_display_button, tile_count_display_button_rect)

    def challenge(self) -> bool:
        button_rect = pygame.Rect(SQUARE_SIZE * 1, SQUARE_SIZE * 18, SQUARE_SIZE * 5.5, SQUARE_SIZE)
        pygame.draw.rect(self.win, WHITE, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 20)
        submit_button = font.render("Challenge Word!", True, BLACK)
        submit_button_rect = font.render("Challenge Word!", True, BLACK)
        submit_button_rect = submit_button.get_rect(center=(4 + (TILE_SIZE * 1.5), SQUARE_SIZE * 18.5))
        self.win.blit(submit_button, button_rect)

        decided = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mpos[0], mpos[1]):
                    while decided is not True:
                        self.draw()
                        valid_rect = pygame.Rect(SQUARE_SIZE * 1, SQUARE_SIZE * 17, TILE_SIZE * 7, TILE_SIZE)
                        pygame.draw.rect(self.win, WHITE, valid_rect)
                        pygame.draw.rect(self.win, BLACK, valid_rect, 1)
                        font = pygame.font.Font('freesansbold.ttf', 22)
                        valid_button = font.render("Is the word valid?", True, BLACK)
                        self.win.blit(valid_button, valid_rect)

                        yes_rect = pygame.Rect(SQUARE_SIZE * 8, SQUARE_SIZE * 17, TILE_SIZE * 2, TILE_SIZE)
                        pygame.draw.rect(self.win, WHITE, yes_rect)
                        pygame.draw.rect(self.win, BLACK, yes_rect, 1)
                        yes_button = font.render("Yes", True, BLACK)
                        self.win.blit(yes_button, yes_rect)

                        no_rect = pygame.Rect(SQUARE_SIZE * 11, SQUARE_SIZE * 17, TILE_SIZE * 2, TILE_SIZE)
                        pygame.draw.rect(self.win, WHITE, no_rect)
                        pygame.draw.rect(self.win, BLACK, no_rect, 1)
                        no_button = font.render("No", True, BLACK)
                        self.win.blit(no_button, no_rect)

                        for event in pygame.event.get():

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mpos = pygame.mouse.get_pos()

                                if yes_rect.collidepoint(mpos[0], mpos[1]):
                                    which_player_rect = pygame.Rect(SQUARE_SIZE * 3, SQUARE_SIZE * 19, TILE_SIZE * 15,
                                                                    TILE_SIZE)
                                    pygame.draw.rect(self.win, WHITE, which_player_rect)
                                    pygame.draw.rect(self.win, BLACK, which_player_rect, 1)
                                    font = pygame.font.Font('freesansbold.ttf', 22)
                                    which_player_button = font.render("Which player number losses their turn?", True,
                                                                      BLACK)
                                    self.win.blit(which_player_button, which_player_rect)

                                    input_rect = pygame.Rect(SQUARE_SIZE * 17, SQUARE_SIZE * 19, TILE_SIZE * 1,
                                                             TILE_SIZE)

                                    input_player_num = ''
                                    player = False
                                    while player is not True:
                                        input_player = font.render(str(input_player_num), True, BLACK)
                                        self.win.blit(input_player, input_rect)

                                        for event in pygame.event.get():

                                            if event.type == pygame.KEYDOWN:

                                                if event.key == pygame.K_BACKSPACE:

                                                    input_player_num = input_player_num[:-1]

                                                elif event.key == pygame.K_RETURN:
                                                    if input_player_num.isdigit() and int(input_player_num)-1 in range(
                                                            len(self._players)):
                                                        self._players[(int(input_player_num)-1)].skip_next_turn = True
                                                        end_time = time.time() + 4
                                                        while time.time() < end_time:
                                                            self.draw()
                                                            lost_turn_rect = pygame.Rect(SQUARE_SIZE * 3,
                                                                                         SQUARE_SIZE * 19,
                                                                                         TILE_SIZE * 7, TILE_SIZE)
                                                            pygame.draw.rect(self.win, WHITE, lost_turn_rect)
                                                            pygame.draw.rect(self.win, BLACK, lost_turn_rect, 1)
                                                            font = pygame.font.Font('freesansbold.ttf', 22)

                                                            lost_turn_button = font.render("Player " + str(
                                                                input_player_num) + " losses turn", True, BLACK)

                                                            self.win.blit(lost_turn_button, lost_turn_rect)
                                                            pygame.display.flip()
                                                        player = True
                                                        return True
                                                else:
                                                    input_player_num += event.unicode
                                            pygame.draw.rect(self.win, WHITE, input_rect)
                                            pygame.draw.rect(self.win, BLACK, input_rect, 1)

                                            input_player = font.render(str(input_player_num), True, BLACK)
                                            self.win.blit(input_player, input_rect)
                                            pygame.display.flip()

                                    self.win.blit(no_button, no_rect)
                                    return True

                                if no_rect.collidepoint((mpos[0], mpos[1])):
                                    for xy in self._placed_tiles:
                                        self._temp_tile = self._board._board[xy[0]][xy[1]]
                                        temp_list = []
                                        temp_list.append(self._temp_tile)
                                        self._tile_bag._tiles_in_bag = self._tile_bag._tiles_in_bag + temp_list
                                        self._board._board[xy[0]][xy[1]] = Tile()
                                        # TODO return new tiles to bag from player hand - complete
                                    end_time = time.time() + 4
                                    while time.time() < end_time:
                                        lost_turn_rect = pygame.Rect(SQUARE_SIZE * 3, SQUARE_SIZE * 19, TILE_SIZE * 8,
                                                                     TILE_SIZE)
                                        pygame.draw.rect(self.win, WHITE, lost_turn_rect)
                                        pygame.draw.rect(self.win, BLACK, lost_turn_rect, 1)
                                        font = pygame.font.Font('freesansbold.ttf', 22)

                                        lost_turn_button = font.render("Player " + str(
                                            self._players[self.current_players_turn].player_num) + " losses turn", True,
                                                                       BLACK)
                                        self.win.blit(lost_turn_button, lost_turn_rect)
                                        pygame.display.flip()
                                        decided = True
                                    return False

                        pygame.display.flip()

    # def clicked_tile(self):
    def pass_button(self, event) -> bool:
        # Draw Pass Button
        button_rect = pygame.Rect(4, SQUARE_SIZE * 14, TILE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, CYAN, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 17)
        pass_button = font.render('Pass Turn', True, BLACK)
        pass_button_rect = pass_button.get_rect(
            center=(4 + (TILE_SIZE * 1.5), SQUARE_SIZE * 14.5))
        self.win.blit(pass_button, pass_button_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mpos[0], mpos[1]):
                self._players[self.current_players_turn].turn_since_last_placement += 1
                return False
        return True

    def discard_button(self) :
        button_rect = pygame.Rect (BOARD_WIDTH, SQUARE_SIZE * 18, SQUARE_SIZE * 3.5, SQUARE_SIZE)
        pygame.draw.rect(self.win, WHITE, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 18)
        discard_button = font.render("Discard Tiles", True, BLACK)
        discard_button_rect = font.render("Discard", True, BLACK)
        discard_button_rect = discard_button.get_rect(center=(BOARD_WIDTH + (SQUARE_SIZE * 1.75), SQUARE_SIZE * 18 + (TILE_SIZE * .5)))
        self.win.blit(discard_button, discard_button_rect)

        mpos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mpos[0], mpos[1]):
            self.clicked=True






    def shuffle_tiles_button(self, event):
        button_rect = pygame.Rect(4, SQUARE_SIZE * 12, TILE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, CYAN, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 16)
        shuffle_button = font.render('Shuffle Tiles', True, BLACK)
        shuffle_button_rect = shuffle_button.get_rect(center=(4 + (TILE_SIZE * 1.5), SQUARE_SIZE * 12.5))
        self.win.blit(shuffle_button, shuffle_button_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mpos[0], mpos[1]):
                self.shuffle_tile_rack()
                return False
        return True

    def reset_word_button(self, event):
        button_rect = pygame.Rect(4, SQUARE_SIZE * 10, TILE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, CYAN, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 16)
        shuffle_button = font.render('Reset Word', True, BLACK)
        shuffle_button_rect = shuffle_button.get_rect(center=(4 + (TILE_SIZE * 1.5), SQUARE_SIZE * 10.5))
        self.win.blit(shuffle_button, shuffle_button_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mpos[0], mpos[1]):
                for xy in self._placed_tiles:
                    self._temp_tile = self._board._board[xy[0]][xy[1]]
                    temp_list = []
                    temp_list.append(self._temp_tile)
                    for player in self._players:
                        if len(player.tile_array) < 7:
                            player.tile_array = player.tile_array + temp_list
                    self._board._board[xy[0]][xy[1]] = Tile()
                return False
        return True

    def end_game(self, event):
        button_rect = pygame.Rect(4, SQUARE_SIZE * 7, TILE_SIZE * 3, SQUARE_SIZE)
        pygame.draw.rect(self.win, LT_MAGENTA, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 18)
        end_game_button = font.render('End Game', True, BLACK)
        end_game_button_rect = end_game_button.get_rect(center=(4 + (TILE_SIZE * 1.5), SQUARE_SIZE * 7.5))
        self.win.blit(end_game_button, end_game_button_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mpos[0], mpos[1]):
                pygame.quit()
                sys.exit()

    def submit_word(self, event) -> bool:
        # Draw Submit word button
        button_rect = pygame.Rect(SQUARE_SIZE, SQUARE_SIZE * 18, SQUARE_SIZE * 5, SQUARE_SIZE)
        pygame.draw.rect(self.win, WHITE, button_rect)
        pygame.draw.rect(self.win, BLACK, button_rect, 1)
        font = pygame.font.Font('freesansbold.ttf', 24)
        submit_button = font.render('Submit Word', True, BLACK)
        submit_button_rect = submit_button.get_rect(center=(SQUARE_SIZE * 3.5, SQUARE_SIZE * 18 + (TILE_SIZE * .5)))
        self.win.blit(submit_button, submit_button_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mpos[0], mpos[1]):
                if len(self._placed_tiles) > 0:
                    self._players[self.current_players_turn].last_placed_word = self._placed_tiles
                    delay = time.time() + 5

                    good_word = None
                    while time.time() < delay and good_word is None:
                        self.draw()
                        good_word = self.challenge()
                        pygame.display.flip()
                    if good_word is None or good_word is True:
                        self._players[self.current_players_turn].score += self.calculate_points(self._board)
                    self._board.draw_scoreboard(self.win, self._players[self.current_players_turn])
                    turn_active = False
                    return turn_active

    def tile_placement(self, tile):
        floating_tile = tile
        placed = False

        while placed is not True:
            mpos = (pygame.mouse.get_pos())

            self.draw()
            tile.draw(self.win, mpos[0], mpos[1])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()

                    mgrid = self.get_row_col_from_mouse(pygame.mouse.get_pos())

                    # board placement
                    if BOARD_OFFSET_X < mpos[0] < BOARD_OFFSET_X + BOARD_WIDTH and BOARD_OFFSET_Y < mpos[
                        1] < BOARD_OFFSET_Y + BOARD_HEIGHT:
                        if self._board._board[int(mgrid[0] - (BOARD_OFFSET_X // SQUARE_SIZE))][
                            int(mgrid[1] - (BOARD_OFFSET_Y // SQUARE_SIZE))].is_tile() is not True:
                            board_grid = (int(mgrid[0] - (BOARD_OFFSET_X // SQUARE_SIZE)),
                                          int(mgrid[1] - (BOARD_OFFSET_Y // SQUARE_SIZE)))
                            self._board.place_tile(tile, board_grid)
                            print(board_grid)
                            self._placed_tiles.append(board_grid)
                            placed = True

    def tile_holder_clicks(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mgrid = self.get_row_col_from_mouse(pygame.mouse.get_pos())

            if TILE_HOLDER_OFFSET_X // SQUARE_SIZE <= mgrid[0] < TILE_HOLDER_OFFSET_X // SQUARE_SIZE + 7 and mgrid[
                1] == TILE_HOLDER_OFFSET_Y // SQUARE_SIZE:
                tile_index = int(mgrid[0] - (TILE_HOLDER_OFFSET_X // SQUARE_SIZE))
                player_tiles = self._players[self.current_players_turn].tile_array

                if player_tiles[tile_index] and player_tiles[tile_index].is_tile():
                    if self.clicked:
                        self._temp_tile = tile_index
                        temp_list = []
                        temp_list.append(self._temp_tile)
                        new_tile = self._tile_bag.get_tiles(1)[0]
                        self._tile_bag._tiles_in_bag = self._tile_bag._tiles_in_bag + temp_list
                        player_tiles[tile_index]=Tile()
                        player_tiles[tile_index]=new_tile
                        self.clicked=False

                    else:
                        self.tile_placement(player_tiles.pop(tile_index))


    def draw(self):
        #pygame.draw.rect(self.win, BLACK, (0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.player_turn_display(self.win)
        self._board.draw(self.win, self._players[self.current_players_turn])
        self.tile_count_display()
        self.discard_button()


    def update(self):
        turn = True
        if self._players[self.current_players_turn].skip_next_turn is True:
            turn = False
            self._players[self.current_players_turn].skip_next_turn = False

        while turn:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.tile_holder_clicks(event)
                self.draw()
                self.shuffle_tiles_button(event)
                self.reset_word_button(event)
                self.end_game(event)


                turn = self.submit_word(event)
                if turn is not False:
                    turn = self.pass_button(event)
                pygame.display.flip()

        self.next_turn()
