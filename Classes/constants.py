import pygame

# Colors by RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
TAN = (238, 232, 170)
MAGENTA = (255, 0, 255)
LT_MAGENTA = (221, 160, 221)
CYAN = (0, 255, 255)
LT_CYAN = (175, 238, 238)
LT_GREY = (230, 230, 230)
YELLOW = (255,255,0)

# Display settings
DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 800

# Board constants
BOARD_WIDTH, BOARD_HEIGHT = DISPLAY_WIDTH * .75, DISPLAY_HEIGHT * .75 # 600

ROWS, COLS = 15, 15
SQUARE_SIZE = (BOARD_WIDTH//COLS) # 40
PLAYER_TILE_TRAY_WIDTH, PLAYER_TILE_TRAY_HEIGHT = SQUARE_SIZE * 7, SQUARE_SIZE

BOARD_OFFSET_X = SQUARE_SIZE * 3
BOARD_OFFSET_Y = SQUARE_SIZE * 2

#Scoreboard size
SCOREBOARD_WIDTH = DISPLAY_WIDTH - (SQUARE_SIZE * 2) #520

#TILE HOLDER SIZE
HOLDER_SIZE_X = SQUARE_SIZE * 7
HOLDER_SIZE_Y = SQUARE_SIZE * 1

# Tile Holder display Constants
TILE_HOLDER_OFFSET_X = SQUARE_SIZE * 7
TILE_HOLDER_OFFSET_Y = SQUARE_SIZE * 18

BOARD_PATTERN =[['TW', '__', '__', 'DL', '__', '__', '__', 'TW', '__', '__', '__', 'DL', '__', '__', 'TW'],
                ['__', 'DW', '__', '__', '__', 'TL', '__', '__', '__', 'TL', '__', '__', '__', 'DW', '__'],
                ['__', '__', 'DW', '__', '__', '__', 'DL', '__', 'DL', '__', '__', '__', 'DW', '__', '__'],
                ['DL', '__', '__', 'DW', '__', '__', '__', 'DL', '__', '__', '__', 'DW', '__', '__', 'DL'],
                ['__', '__', '__', '__', 'DW', '__', '__', '__', '__', '__', 'DW', '__', '__', '__', '__'],
                ['__', 'TL', '__', '__', '__', 'TL', '__', '__', '__', 'TL', '__', '__', '__', 'TL', '__'],
                ['__', '__', 'DL', '__', '__', '__', 'DL', '__', 'DL', '__', '__', '__', 'DL', '__', '__'],
                ['TW', '__', '__', 'DL', '__', '__', '__', 'ST', '__', '__', '__', 'DL', '__', '__', 'TW'],
                ['__', '__', 'DL', '__', '__', '__', 'DL', '__', 'DL', '__', '__', '__', 'DL', '__', '__'],
                ['__', 'TL', '__', '__', '__', 'TL', '__', '__', '__', 'TL', '__', '__', '__', 'TL', '__'],
                ['__', '__', '__', '__', 'DW', '__', '__', '__', '__', '__', 'DW', '__', '__', '__', '__'],
                ['DL', '__', '__', 'DW', '__', '__', '__', 'DL', '__', '__', '__', 'DW', '__', '__', 'DL'],
                ['__', '__', 'DW', '__', '__', '__', 'DL', '__', 'DL', '__', '__', '__', 'DW', '__', '__'],
                ['__', 'DW', '__', '__', '__', 'TL', '__', '__', '__', 'TL', '__', '__', '__', 'DW', '__'],
                ['TW', '__', '__', 'DL', '__', '__', '__', 'TW', '__', '__', '__', 'DL', '__', '__', 'TW']]

PLAYER1_TILE_BOARD = ['P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17']
PLAYER2_TILE_BOARD = ['P21', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27']
PLAYER3_TILE_BOARD = ['P31', 'P32', 'P33', 'P34', 'P35', 'P36', 'P37']
PLAYER4_TILE_BOARD = ['P41', 'P42', 'P43', 'P44', 'P45', 'P46', 'P47']

VALID_MOVES = ['ST', 'TW', 'DW', 'TL', 'DL', '__']


# Tile constants
TILE_SIZE = SQUARE_SIZE-4
# TILE_FONT = pygame.font.Font('freesansbold.ttf', 32)  # Parameters: Font and font size

TILE_BAG_COUNTS = {'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4,
                   'M': 2, 'N': 6, 'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1,
                   'Y': 2, 'Z': 1, '_': 2}

TILE_SCORES = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3,
               'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10,
               '_': 0, '': 0}


# Player constants
MAX_PLAYERS = 2    # Max players is used for testing purposes
MAX_TILES_PLAYABLE = 7
# PLAYER_NAME_FONT = pygame.font.Font('freesansbold.ttf', 32)
PLAYER_TEXTX, PLAYER_TEXTY = 150, 10
