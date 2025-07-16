# Console Battleship Game Specifications
## Game Overview:

The game is a simplified version of the classic Battleship board game.

It is played on a grid where players place ships and attempt to guess the locations of their opponent's ships.

## Game Components:

### Grid:
A 2D grid (15 x 10) representing the game board.

Each cell on the grid represents a position on the board.

The grid is hidden from the opponent during gameplay.

### Ships:
Each player has a set of ships to place on their grid.

Ships have different sizes: 2 cells, 3 cells, 4 cells, and 5 cells.

Ships cannot overlap or be placed diagonally.

### Player Interaction:
Players take turns to perform actions.

On their turn, a player chooses a cell on the opponent's grid to target.

The player receives feedback on whether the target was a hit or a miss.

### Hit/Miss Feedback:
If a player's target hits a ship, they receive a hit notification.

If a player's target misses all ships, they receive a miss notification.

### Win Condition:
The game continues until one player's ships are all sunk.

A player's ship is considered sunk when all cells occupied by that ship have been hit.

### Game Flow:

#### Setup Phase:

Players type in a non empty string of characters with their name.

Players are asked to place their ships on their respective grids.

Ships can be placed horizontally or vertically.

Players cannot see each other's grids during setup.

#### Gameplay Phase:

Players take turns selecting cells on the opponent's grid to attack.

After each attack, players receive feedback on whether they hit or missed a ship.

Players alternate turns until one player's ships are all sunk.

### End Game:

When one player's ships are all sunk, the game ends.

The winning player is declared, and the game terminates.

### User Interactions: 

#### Menu System:

The game should start with a menu system that shows instructions, asks each player in turn to insert a valid string representing their name, or exit the game.

The menu should be easy to navigate and understand.

#### Input Handling:

The game should handle player input for actions such as placing ships, targeting opponent's grid and view game instructions.

Input should be validated to ensure it falls within acceptable ranges and formats.

Error messages should be displayed for invalid input, guiding the player on how to correct it.

#### Visual Feedback:
Provide clear visual feedback to the player for each action they perform.

Display the game grid(s) with appropriate symbols to represent ships, hits, misses, and empty cells. The following are required:

            'I' - injured cell of the ship

            'D' - dead ship

            'H' - healthy part of the ship

            'M' - miss

            '~' - untouched cell on the field

(Desirable) it the use of color-coding or other visual cues to distinguish between different states of the game (e.g., ship placement phase, gameplay phase, end game).

#### Text-based Instructions:

Include text-based instructions or prompts to guide the player through various stages of the game.

Instructions should be concise, clear, and easy to understand.

Players should be able to access instructions or help information from the main menu or during gameplay.

#### Turn-Based Interaction:

During gameplay, the game should clearly indicate whose turn it is to take an action.

Players should be prompted to input their actions (e.g., selecting a cell to target) when it's their turn.

After each action, the game should update the display to show the current state of the game board and provide feedback on the action taken.

#### Game Progression:
The game should provide feedback on the progression of the game (e.g., remaining ships, number of hits/misses).

Players should be informed of important events such as sinking an opponent's ship or winning the game.

#### End Game Interaction:
When the game ends, display the final outcome (e.g., victory, defeat) to the player.

Allow players to choose whether they want to play again, return to the main menu, or exit the game.

#### Error Handling:
Handle unexpected errors or exceptions gracefully to prevent crashes or unexpected behavior.

Provide informative error messages to the player in case of errors that require user intervention (e.g., invalid input).
