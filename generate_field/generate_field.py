import random
from .common import is_correct_cell

# Based on ship Length and Start cell, this function determines the possible directions and append them to the results 
# For example: a 2 length ship in a 3 x 3 field, placed at (1,1)
# The only possible directions are Right (0, 1) and bottom (1, 0)
def possible_direction(ship_length, allowed_cells, start_cell):
    """
    int, set(tuple(int, int)), tuple(int, int) -> list(tuple(int, int))

    returns list of all possible directions in which ship with length
    ship_length can be placed

    allowed cells is a set of cells which can be used

    if we cannot build the ship in any direction, returns None

    structure of directions:
        1) (0, 1) - to the right
        2) (0, -1) - to the left
        3) (1, 0) - to the bottom
        4) (-1, 0) - to the top
    """
    possible_directions = set([(0, 1), (0, -1), (1, 0), (-1, 0)])
    result = []
    for current_direction in possible_directions:
        is_ok = True
        for i in range(1, ship_length):
            current_cell = (start_cell[0] + current_direction[0] * i,       # Place verticle cell
                            start_cell[1] + current_direction[1] * i)       # Place horizontal cell
            if (not is_correct_cell(current_cell) or
                    current_cell not in allowed_cells):
                is_ok = False
                break
        if is_ok:
            result.append(current_direction)
    if len(result) == 0:
        return None
    return result


def write_ship(allowed_cells,
               current_battlefield,
               start_cell,
               ship_length,
               direction=(0, 0)):
    """
    set(tuple(int, int)),
    dict(tuple(int, int): None or bool),
    tuple(int, int), int,
    tuple(int, int) -> None

    updates allowed cells and current_battlefield writing
    a ship with length ship_length
    from start_cell in direction direction

    read more about direction in possible_direction() documentation
    read more about current_battlefield in generate_field() documentation
    """
    for i in range(ship_length):                                         # Set False in the current_battlefield dic to identify ship location
        current_cell = (start_cell[0] + i * direction[0],
                        start_cell[1] + i * direction[1])
        current_battlefield[current_cell] = False                        # At i = 0 ==> Sets the Ship start cell

    end_cell = (start_cell[0] + (ship_length - 1) * direction[0],        # Determine the end cell Location
                start_cell[1] + (ship_length - 1) * direction[1])

    delete_start_cell = (min(start_cell[0], end_cell[0]) - 1,
                         min(start_cell[1], end_cell[1]) - 1)

    delete_end_cell = (max(start_cell[0], end_cell[0]) + 1,
                       max(start_cell[1], end_cell[1]) + 1)

    for row in range(delete_start_cell[0], delete_end_cell[0] + 1):       # Remove the cells which the ship have been placed at (False) and a zone around it
        for col in range(delete_start_cell[1], delete_end_cell[1] + 1):
            if (row, col) in allowed_cells:
                allowed_cells.remove((row, col))


def generate_field():
    """
    () -> dict(tuple(int, int): None or bool)

    generates random battlefield and returns it
    it is guaranteed that the placement of all the ships is according
    to all the rules in battleship game

    dictionary structure:
        - the key is (int, int) - number of row and column respectively
        - numbers in key are in [1; 10] inclusive
        - the value can be:
            1) None - there is nothing in that cell
            2) False - there is undamaged ship in that cell
            3) True - there is damaged ship in that cell
    """
    allowed_cells = set()
    ship_rules = {4: 1, 3: 2, 2: 3, 1: 4}               # One size 4 + Two size 3 + Three size 2 + Four size 1
    current_battlefield = {}
    for i in range(1, 11):
        for j in range(1, 11):
            allowed_cells.add((i, j))                   # Create a set of field locations {(1,1),(1,2),.....(10,10)}
            current_battlefield[(i, j)] = None          # Creat a dic {(1,1): None, {1,2}: None.,,,,. {10,10}: None}

    for ship_length in range(4, 1, -1):
        allowed_guess = allowed_cells.copy()            # Copy set
        for i in range(ship_rules[ship_length]):
            while allowed_guess:
                random_cell = random.sample(list(allowed_guess), 1)[0]            # Select a random cell for example (5,1) from the start cell
                current_result = possible_direction(ship_length,            # Return the possible directions right (0,1) and bottom (-1,0)
                                                    allowed_cells,
                                                    random_cell)
                
                if current_result is None:                                  # this means there where no possible directions for this ship length
                    allowed_guess.remove(random_cell)                       # at this start cell so remove from cell from allowed guess
                else:
                    write_ship(allowed_cells,                               # Write cell in allowed cells
                               current_battlefield,
                               random_cell,                                 # Select a random cell for example (5,1) for the start cell
                               ship_length,
                               random.choice(current_result))               # Randomly determine possible direction
                    allowed_guess = allowed_cells.copy()\
                        .intersection(allowed_guess)                        # Update the allowed guess with the new avilable cells after placing the ship
                    break

    for i in range(4):                                                      # Write Ships with Length 1 randomly
        write_ship(allowed_cells,
                   current_battlefield,
                   random.sample(list(allowed_cells), 1)[0],                       # Select a random cell for example (5,1) for the start cell
                   1)
    return current_battlefield
