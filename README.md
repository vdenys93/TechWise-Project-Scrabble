Added - 3 August 2022

	Continued PEP 8 organization and structuring.
	
	Added tile tray refil feature and increased functionality

Added  - 21 Jul 2022

   Changed background color to distinguish the board from the background display
   Added Text to the base board tiles.  

   NOTE:  ST is temporarily changed with a manual example of the code for a Letter placement (E)


Added- 20 Jul 2022

   Added Game Class for game mechanics
   Began game mechanic for mouse tile movement

   board.py:
   Added get_tile method
   Added create_board method
   Added move method
   Added place for player tiles - not sure how this will work with the grid system.  Needs tested when tiles are ready.
   
   game.py:
   Added update()
   Added reset()
   Added select() - to select tiles
   Added _move()
   Added change_turn()
   
   tiles.py:
   Added calc_position()
   Added draw_tile()
   Added move()


Added  - 19 July 2022:

   Created/ Modified Files:
   
   Created a base game structure
   Added init.py file to main folder
   Modified main to work with board and constants file
   Created a scrabble game sub module
      Created init.py in submodule
      Created Board and Tiles Classes
      Created constants.py to store and organize constants used throughout the game


Notes:
Game board designed with basic features.  Game board is a percentage of the display screen and can become 
scalable with increased board size or if fixed to a display size.

Board has grids and tiles of base colors for different board features, Double & Triple Word, 
and Double & Triple Letter Scores.  Board also has a place-holder for the star in the center.  
Coordinate system on board is tested and working.  Board[row][col]

Currently, adjustments are still made through the constants.py file


