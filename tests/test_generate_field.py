import random
import pytest
from generate_field.common import is_correct_cell
from generate_field.generate_field import possible_direction
from generate_field.generate_field import write_ship
from generate_field.generate_field import generate_field

class Tests_generate_field:
    ##############################################################################################################
    # possible_direction function Tests
    @pytest.mark.parametrize("ship_length,start_cell,expected_result",[
        (4,(5,5),[(0,1),(0,-1),(1,0),(-1,0)]),
        (3,(5,5),[(0,1),(0,-1),(1,0),(-1,0)]),
        (2,(5,5),[(0,1),(0,-1),(1,0),(-1,0)]),
        (1,(5,5),[(0,1),(0,-1),(1,0),(-1,0)]),
    ])
    def test_possible_direction(self,ship_length,start_cell,expected_result ):
        '''
        do: Test the possible_direction when the ship_length is (4,3,2,1) at the start_cell = (5,5)
        logic: Basic functionality test that aims to verify the possible_direction function returned 
        list values for ships with different sizes when placed at the center of the field (5,5)
        '''
        # Step #1: Setup the values of allowed_cells
        allowed_cells = {(i, j) for i in range(1, 11) for j in range(1, 11)}
        
        # Step #2: Setup the results
        result = possible_direction(ship_length,allowed_cells,start_cell)

        # Step #3: Confirm Results
        assert set(result) == set(expected_result)  # Convert list to set to compare contents without considering the contents order


    @pytest.mark.parametrize("ship_length,start_cell,expected_result",[
        (1,(1,1),[(0,1),(0,-1),(1,0),(-1,0)]),            # Right, Left Bottom and Top
        (2,(1,10),[(0,-1),(1,0)]),                        # Left and Bottom
        (3,(10,1),[(0,1),(-1,0)]),                        # Right and Top
        (4,(10,10),[(0,-1),(-1,0)]),                      # Left and Top
    ])
    def test_possible_direction_corner_cases(self,ship_length,start_cell,expected_result ):
        '''
        do: Test the possible_direction function for all ship lengths when the start cell is at a the edge of the boundry.
        Place ship_length 1 at (1,1), shipe_length 2 at (1,10), shipe_length 3 at (10,1) and shipe_length 4 at (10,10). 
        logic: Test the possible_direction function when the ship is placed at the edge of the boundry. Check diagram below:
        x represent the start cell of each ship.
        ------------------------------------
                    cell format
                1 2 3 4 5 6 7 8 9 10
            1   x                 x
            2
            3
            4
            5
            6
            7
            8
            9
            10  x                  x
        '''
        # Step #1: Setup the values of allowed_cells
        allowed_cells = {(i, j) for i in range(1, 11) for j in range(1, 11)}

        # Step #2: Setup the results
        result = possible_direction(ship_length,allowed_cells,start_cell)

        # Step #3: Confirm Results
        assert set(result) == set(expected_result)  # Convert list to set to compare contents without considering the contents order

    @pytest.mark.xfail
    @pytest.mark.parametrize("ship_length,start_cell",[
        (11,(15,15)),            # Invalid Ship_length and Invalid Start_cell
        (11,(1,1)),              # Invalid Ship_length and Valid Start_cell
        (4,(11,1))               # Valid Ship_length and Invalid Start_cell ==> returns [(-1,0)] - This is a bug
    ])
    def test_possible_direction_invalid_input(self,ship_length,start_cell ):
        '''
        do: Test the function if argument ship_length is Invalid (not 1,2,3,4) and the start cell is outside the specifed 
        allowed cells ==> {(1,1),....,(10,10)}
        Logic: confirm that the function returns None when the arguments are Invalid (outside the specifed boundries).
        ***Bug: This test revealed that when the ship_length is 4 and start_cell is (11,1), the function returns [(-1,0)]
        this is a bug that the design team should be notified of!!
        '''
        # Step #1: Setup the values of allowed_cells
        allowed_cells = {(i, j) for i in range(1, 11) for j in range(1, 11)}
        
        # Step #2: Setup the results
        result = possible_direction(ship_length,allowed_cells,start_cell)

        # Step #3: Confirm Results
        assert result == None

    @pytest.mark.parametrize("ship_length,allowed_cells,start_cell",[
            ("Four","Any_Field","A55"),     
            (3,"Any_Field",(1,1)),
            ("Four",{(1,1),(1,2),(2,1),(2,2)},(1,1))
    ])
    def test_possible_direction_type_error(self,ship_length, allowed_cells, start_cell):
        '''
        do: Test the function if input is NOT ==> int, set(tuple(int, int)), tuple(int, int)
        Logic: This test aims to confirm that the possible_direction function raises a 
        TypeError when the passed argument types are not as expected by function.
        '''
        with pytest.raises(TypeError):
            possible_direction(ship_length, allowed_cells, start_cell)

    @pytest.mark.parametrize("ship_length,start_cell,expected_result",[
        (2,(1,1),[(0,1)])
    ])
    def test_possible_direction_prime_path_A(self, ship_length,start_cell,expected_result ):
        '''
        do: Test the possible_direction when the ship_length is 2 at the start_cell = (1,1)
        logic: Setup a the function input to generate a Test path that includes prime paths.
        - This test passes by nodes [1, 2, 3, 4, 5, 6, 4, 8, 9, 2, 3, 4, 5, 6, 7, 4, 8, 2, 3, 4, 5, 6, 7, 4, 
                                     8, 2, 3, 4, 5, 6, 7, 4, 8, 2, 10, 12]
        - The Prime Path includes within this path are:
            1. Prime Path 1 = [5, 6, 4, 8, 9, 2, 3]
            2. Prime Path 2 = [4, 8, 9, 2, 3, 4]
            3. Prime Path 3 = [4, 8, 2, 3, 4]
            4. Priime Path 4 = [4, 5, 6, 4]
        '''
        # Step #1: Setup the values of allowed_cells
        allowed_cells = {(1, 1), (1, 2), (2, 2)}
        
        # Step #2: Setup the results
        result = possible_direction(ship_length,allowed_cells,start_cell)

        # Step #3: Confirm Results
        # Convert list to set to compare contents without considering the contents order
        assert set(result) == set(expected_result)  

    @pytest.mark.parametrize("ship_length,start_cell,expected_result",[
        (2,(2, 2),[(0,1),(0,-1),(1,0),(-1,0)])
    ])
    def test_possible_direction_prime_path_B(self, ship_length,start_cell,expected_result ):
        '''
        do: Test the possible_direction when the ship_length is 2 at the start_cell = (2,2)
        logic: Setup a the function input to generate a Test path that includes prime paths.
        - This test passes by nodes 
        - The Prime Path includes within this path are: [1, 2, 3, 4, 5, 6, 4, 8, 9, 2, 3, 4, 5, 6, 
                                                         4, 8, 9, 2, 3, 4, 5, 6, 4, 8, 9, 2,3, 4, 5, 
                                                         6, 4, 8, 9, 2, 10, 12]
            1. Prime Path 1 = [5, 6, 4, 8, 9, 2, 10, 12]
            2. Prime Path 2 = [5, 6, 4, 8, 9, 2, 3]
            3. Prime Path 3 = [4, 8, 9, 2, 3, 4]
            4. Priime Path 4 = [4, 5, 6, 4]
        '''
        # Step #1: Setup the values of allowed_cells
        allowed_cells = {(i, j) for i in range(1, 4) for j in range(1, 4)}
        
        # Step #2: Setup the results
        result = possible_direction(ship_length,allowed_cells,start_cell)

        # Step #3: Confirm Results
        # Convert list to set to compare contents without considering the contents order
        assert set(result) == set(expected_result)  




    ##############################################################################################################
    # write_ships function Tests
    def test_write_ship_len_4_right(self):
        '''
        do: Confirm the write_ship function correctly updates the allowed_cells and current_battlefield when ship length is 4 and direction is right.
        Logic: Manually determine the allowed_cells and current_battlefield contents from the write_ship function logic.
        Then,compare the results derived manually with the values returned from the write_ship function.
        '''
        # Step 1: Setup the function arguments (inputs)
        allowed_cells =  {(i, j) for i in range(1, 11) for j in range(1, 11)}                   # Generate a 10x10 allowed cells
        current_battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}        # Set all current_battlefield values to None
        start_cell = (1, 1)                                                                     # Set start cell
        ship_length = 4                                                                         # Set ship length
        direction = (0, 1)                                                                      # Set direction: Horizontal right

        # Step 2: Expected resulst - manually determined from function logic
        expected_battlefield = {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): None, 
                                (1, 6): None, (1, 7): None, (1, 8): None, (1, 9): None, (1, 10): None, 
                                (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, 
                                (2, 6): None, (2, 7): None, (2, 8): None, (2, 9): None, (2, 10): None, 
                                (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (3, 6): None, 
                                (3, 7): None, (3, 8): None, (3, 9): None, (3, 10): None, (4, 1): None, (4, 2): None, 
                                (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (4, 9): None, 
                                (4, 10): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): None, (5, 6): None, 
                                (5, 7): None, (5, 8): None, (5, 9): None, (5, 10): None, (6, 1): None, (6, 2): None, (6, 3): None, 
                                (6, 4): None, (6, 5): None, (6, 6): None, (6, 7): None, (6, 8): None, (6, 9): None, (6, 10): None, 
                                (7, 1): None, (7, 2): None, (7, 3): None, (7, 4): None, (7, 5): None, (7, 6): None, (7, 7): None, 
                                (7, 8): None, (7, 9): None, (7, 10): None, (8, 1): None, (8, 2): None, (8, 3): None, (8, 4): None, 
                                (8, 5): None, (8, 6): None, (8, 7): None, (8, 8): None, (8, 9): None, (8, 10): None, (9, 1): None, 
                                (9, 2): None, (9, 3): None, (9, 4): None, (9, 5): None, (9, 6): None, (9, 7): None, (9, 8): None, 
                                (9, 9): None, (9, 10): None, (10, 1): None, (10, 2): None, (10, 3): None, (10, 4): None, 
                                (10, 5): None, (10, 6): None, (10, 7): None, (10, 8): None, (10, 9): None, (10, 10): None}
        expected_allowed_cells = {(4, 9), (5, 1), (5, 10), (8, 9), (10, 6), (9, 8), (6, 2), (7, 1), (7, 10), (4, 2), (3, 6), 
                                  (5, 3), (8, 2), (9, 1), (9, 10), (1, 8), (6, 4), (7, 3), (3, 8), (5, 5), (8, 4), (9, 3), (1, 10), 
                                  (6, 6), (7, 5), (3, 1), (3, 10), (5, 7), (9, 5), (7, 7), (3, 3), (5, 9), (9, 7), (10, 8), (6, 1), 
                                  (7, 9), (3, 5), (5, 2), (4, 4), (9, 9), (10, 1), (10, 10), (1, 7), (2, 6), (7, 2), (3, 7), (5, 4), 
                                  (4, 6), (9, 2), (8, 6), (10, 3), (1, 9), (2, 8), (7, 4), (6, 8), (3, 9), (5, 6), (4, 8), (8, 8), 
                                  (10, 5), (2, 10), (6, 10), (3, 2), (4, 1), (4, 10), (8, 1), (8, 10), (10, 7), (6, 3), (3, 4), (4, 3), 
                                  (8, 3), (10, 9), (1, 6), (6, 5), (4, 5), (8, 5), (10, 2), (9, 4), (2, 7), (6, 7), (7, 6), (4, 7), 
                                  (5, 8), (8, 7), (10, 4), (9, 6), (2, 9), (6, 9), (7, 8)}

        # Step 3: Call write_ship function
        write_ship(allowed_cells, current_battlefield, start_cell, ship_length, direction)

        # Step 4: Check Results
        assert current_battlefield == expected_battlefield
        assert allowed_cells == expected_allowed_cells

    def test_write_ship_len_3_bottom(self):
        '''
        do: Test the write_ship function allowed_cells and current_battlefield when ship length is 3 and direction is bottom
        Logic: Manually determine the allowed_cells and current_battlefield contents from the write_ship function logic.
        Then,compare the manual results with the values returned from the write_ship function.
        '''
        # Step 1: Setup the function arguments (inputs)
        allowed_cells =  {(i, j) for i in range(1, 11) for j in range(1, 11)}                   # Generate a 10x10 allowed cells
        current_battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}        # Set all current_battlefield values to None
        start_cell = (5, 5)                                                                     # Set start cell
        ship_length = 3                                                                         # Set ship length
        direction = (1, 0)                                                                      # Horizontal bottom

        # Step 2: Expected results - manually determined from function logic
        expected_battlefield = {(1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (1, 5): None, (1, 6): None, (1, 7): None, (1, 8): None, (1, 9): None, (1, 10): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (2, 7): None, (2, 8): None, (2, 9): None, (2, 10): None, (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (3, 6): None, (3, 7): None, (3, 8): None, (3, 9): None, (3, 10): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (4, 9): None, (4, 10): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): False, (5, 6): None, (5, 7): None, (5, 8): None, (5, 9): None, (5, 10): None, (6, 1): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 5): False, (6, 6): None, (6, 7): None, (6, 8): None, (6, 9): None, (6, 10): None, (7, 1): None, (7, 2): None, (7, 3): None, (7, 4): None, (7, 5): False, (7, 6): None, (7, 7): None, (7, 8): None, (7, 9): None, (7, 10): None, (8, 1): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 5): None, (8, 6): None, (8, 7): None, (8, 8): None, (8, 9): None, (8, 10): None, (9, 1): None, (9, 2): None, (9, 3): None, (9, 4): None, (9, 5): None, (9, 6): None, (9, 7): None, (9, 8): None, (9, 9): None, (9, 10): None, (10, 1): None, (10, 2): None, (10, 3): None, (10, 4): None, (10, 5): None, (10, 6): None, (10, 7): None, (10, 8): None, (10, 9): None, (10, 10): None}
        expected_allowed_cells = {(4, 9), (5, 1), (5, 10), (8, 9), (10, 6), (9, 8), (2, 2), (6, 2), (7, 1), (7, 10), (4, 2), (3, 6), (5, 3), (8, 2), (9, 1), (9, 10), (2, 4), (1, 8), (7, 3), (3, 8), (9, 3), (1, 10), (3, 1), (3, 10), (5, 7), (9, 5), (1, 3), (7, 7), (3, 3), (5, 9), (9, 7), (10, 8), (1, 5), (6, 1), (7, 9), (3, 5), (5, 2), (9, 9), (10, 1), (10, 10), (1, 7), (2, 6), (7, 2), (3, 7), (9, 2), (10, 3), (1, 9), (2, 8), (6, 8), (3, 9), (4, 8), (8, 8), (10, 5), (1, 2), (2, 1), (2, 10), (6, 10), (3, 2), (4, 1), (4, 10), (8, 1), (8, 10), (10, 7), (1, 4), (2, 3), (6, 3), (3, 4), (4, 3), (8, 3), (10, 9), (1, 6), (2, 5), (10, 2), (9, 4), (2, 7), (6, 7), (4, 7), (5, 8), (8, 7), (10, 4), (1, 1), (9, 6), (2, 9), (6, 9), (7, 8)}

        # Step 3: Call the function
        write_ship(allowed_cells, current_battlefield, start_cell, ship_length, direction)

        # Step 4: Check Results
        assert current_battlefield == expected_battlefield
        assert allowed_cells == expected_allowed_cells

    def test_write_ship_len_2_top(self):
        '''
        do: Test the write_ship function allowed_cells and current_battlefield when ship length is 2 and direction is top.
        Logic: Manually determine the allowed_cells and current_battlefield contents from the write_ship function logic.
        Then,compare the manual results with the values returned from the write_ship function.
        '''
        # Step 1: Setup the function arguments (inputs)
        allowed_cells =  {(i, j) for i in range(1, 11) for j in range(1, 11)}                   # Generate a 10x10 allowed cells
        current_battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}        # Set all current_battlefield values to None
        start_cell = (10, 10)                                                                   # Set start cell
        ship_length = 2                                                                         # Set ship length
        direction = (-1, 0)                                                                     # Horizontal top

        # Step 2: Expected resulst - manually determined from function logic
        expected_battlefield = {(1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (1, 5): None, (1, 6): None, (1, 7): None, (1, 8): None, (1, 9): None, (1, 10): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (2, 7): None, (2, 8): None, (2, 9): None, (2, 10): None, (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (3, 6): None, (3, 7): None, (3, 8): None, (3, 9): None, (3, 10): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (4, 9): None, (4, 10): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): None, (5, 6): None, (5, 7): None, (5, 8): None, (5, 9): None, (5, 10): None, (6, 1): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 7): None, (6, 8): None, (6, 9): None, (6, 10): None, (7, 1): None, (7, 2): None, (7, 3): None, (7, 4): None, (7, 5): None, (7, 6): None, (7, 7): None, (7, 8): None, (7, 9): None, (7, 10): None, (8, 1): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 5): None, (8, 6): None, (8, 7): None, (8, 8): None, (8, 9): None, (8, 10): None, (9, 1): None, (9, 2): None, (9, 3): None, (9, 4): None, (9, 5): None, (9, 6): None, (9, 7): None, (9, 8): None, (9, 9): None, (9, 10): False, (10, 1): None, (10, 2): None, (10, 3): None, (10, 4): None, (10, 5): None, (10, 6): None, (10, 7): None, (10, 8): None, (10, 9): None, (10, 10): False}
        expected_allowed_cells = {(4, 9), (5, 1), (5, 10), (10, 6), (9, 8), (2, 2), (6, 2), (7, 1), (7, 10), (4, 2), (3, 6), (5, 3), (8, 2), (9, 1), (2, 4), (1, 8), (6, 4), (7, 3), (3, 8), (5, 5), (8, 4), (9, 3), (1, 10), (6, 6), (7, 5), (3, 1), (3, 10), (5, 7), (9, 5), (1, 3), (7, 7), (3, 3), (5, 9), (9, 7), (10, 8), (1, 5), (6, 1), (7, 9), (3, 5), (5, 2), (4, 4), (10, 1), (1, 7), (2, 6), (7, 2), (3, 7), (5, 4), (4, 6), (9, 2), (8, 6), (10, 3), (1, 9), (2, 8), (7, 4), (6, 8), (3, 9), (5, 6), (4, 8), (8, 8), (10, 5), (1, 2), (2, 1), (2, 10), (6, 10), (3, 2), (4, 1), (4, 10), (8, 1), (10, 7), (1, 4), (2, 3), (6, 3), (3, 4), (4, 3), (8, 3), (1, 6), (2, 5), (6, 5), (4, 5), (8, 5), (10, 2), (9, 4), (2, 7), (6, 7), (7, 6), (4, 7), (5, 8), (8, 7), (10, 4), (1, 1), (9, 6), (2, 9), (6, 9), (7, 8)}

        # Step 3: Call the function
        write_ship(allowed_cells, current_battlefield, start_cell, ship_length, direction)

        # Step 4: Check Results
        assert current_battlefield == expected_battlefield
        assert allowed_cells == expected_allowed_cells

    def test_write_ship_len_1_left(self):
        '''
        do: Test the write_ship function allowed_cells and current_battlefield when ship length is 1 and direction is left
        Logic: Manually determine the allowed_cells and current_battlefield contents from the write_ship function logic.
        Then,compare the manual results with the values returned from the write_ship function.
        '''
        # Step 1: Setup the function arguments (inputs)
        allowed_cells =  {(i, j) for i in range(1, 11) for j in range(1, 11)}                   # Generate a 10x10 allowed cells
        current_battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}        # Set all current_battlefield values to None
        start_cell = (7, 6)                                                                     # Set start cell
        ship_length = 1                                                                         # Set ship length
        direction = (0, -1)                                                                     # Horizontal left

        # Step 2: Expected resulst - manually determined from function logic
        expected_battlefield = {(1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (1, 5): None, (1, 6): None, (1, 7): None, (1, 8): None, (1, 9): None, (1, 10): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (2, 7): None, (2, 8): None, (2, 9): None, (2, 10): None, (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (3, 6): None, (3, 7): None, (3, 8): None, (3, 9): None, (3, 10): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (4, 9): None, (4, 10): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): None, (5, 6): None, (5, 7): None, (5, 8): None, (5, 9): None, (5, 10): None, (6, 1): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 7): None, (6, 8): None, (6, 9): None, (6, 10): None, (7, 1): None, (7, 2): None, (7, 3): None, (7, 4): None, (7, 5): None, (7, 6): False, (7, 7): None, (7, 8): None, (7, 9): None, (7, 10): None, (8, 1): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 5): None, (8, 6): None, (8, 7): None, (8, 8): None, (8, 9): None, (8, 10): None, (9, 1): None, (9, 2): None, (9, 3): None, (9, 4): None, (9, 5): None, (9, 6): None, (9, 7): None, (9, 8): None, (9, 9): None, (9, 10): None, (10, 1): None, (10, 2): None, (10, 3): None, (10, 4): None, (10, 5): None, (10, 6): None, (10, 7): None, (10, 8): None, (10, 9): None, (10, 10): None}
        expected_allowed_cells = {(4, 9), (5, 1), (5, 10), (8, 9), (10, 6), (9, 8), (2, 2), (6, 2), (7, 1), (7, 10), (4, 2), (3, 6), (5, 3), (8, 2), (9, 1), (9, 10), (2, 4), (1, 8), (6, 4), (7, 3), (3, 8), (5, 5), (8, 4), (9, 3), (1, 10), (3, 1), (3, 10), (5, 7), (9, 5), (1, 3), (3, 3), (5, 9), (9, 7), (10, 8), (1, 5), (6, 1), (7, 9), (3, 5), (5, 2), (4, 4), (9, 9), (10, 1), (10, 10), (1, 7), (2, 6), (7, 2), (3, 7), (5, 4), (4, 6), (9, 2), (10, 3), (1, 9), (2, 8), (7, 4), (6, 8), (3, 9), (5, 6), (4, 8), (8, 8), (10, 5), (1, 2), (2, 1), (2, 10), (6, 10), (3, 2), (4, 1), (4, 10), (8, 1), (8, 10), (10, 7), (1, 4), (2, 3), (6, 3), (3, 4), (4, 3), (8, 3), (10, 9), (1, 6), (2, 5), (4, 5), (10, 2), (9, 4), (2, 7), (4, 7), (5, 8), (10, 4), (1, 1), (9, 6), (2, 9), (6, 9), (7, 8)}

        # Step 3: Call the function
        write_ship(allowed_cells, current_battlefield, start_cell, ship_length, direction)

        # Step 4: Check Results
        assert current_battlefield == expected_battlefield
        assert allowed_cells == expected_allowed_cells

    @pytest.mark.xfail(reson="write_ship function do not raise an error when start_cell is not in allowed cells")
    def test_write_ship_outside_start_cell(self):
        '''
        do: Place a start_cell outside the allowed_cells and check the write_ship function allowed_cells and current_battlefield values.
        Logic: Intentionally place a start cell outside of the allowed cells and check if the function raise an error or not
        ***Bug: The cell did not recognise that the start cell is outside of the allowed cells, this is a bug that the design team should be notified of!!
        '''
        # Step 1: Setup the function arguments (inputs)
        allowed_cells =  {(i, j) for i in range(1, 11) for j in range(1, 11)}                   # Generate a 10x10 allowed cells
        current_battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}        # Set all current_battlefield values to None
        start_cell = (-5, -12)                                                                  # Set start cell
        ship_length = 4                                                                         # Set ship length
        direction = (0, 1)                                                                      # Horizontal right

        # Step 2: Expected resulst - manually determined from function logic
        expected_battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}
        expected_allowed_cells = {(i, j) for i in range(1, 11) for j in range(1, 11)}

        # Step 3: Call the function
        write_ship(allowed_cells, current_battlefield, start_cell, ship_length, direction)

        # Step 4: Check Results
        assert (current_battlefield == expected_battlefield) and (allowed_cells == expected_allowed_cells)

    ##############################################################################################################
    # generate_field function Tests
    def test_generate_field(self):
        '''
        do: Call generate_field and analyis the returned dictionary contents (current_battlefield)
        logic: Aim is to verify that the rule games are followed for the randomly generated battlefield
        the checks include:
            1. Confirm that a 10x10 field was generated.
            2. Confirm that 20 cells have been set to False (contain Healthy ships in the cell).
               NB: 20 is derived from (4x1)+(3x2)+(2x3)+(1x4)= 20 cells.
        '''
        # Step #1: Call Function
        results = generate_field()

        # Step #2: Logic to check the contents of the results
        results_values_False_count = 0
        results_keys = set()

        for i in results.values():
            if i == False:
                results_values_False_count += 1
        
        for i in results.keys():
            results_keys.add(i)

        # Step #3: Set expected Results
        Expected_Results_False_count = 20
        Expected_Results_Keys = {(i, j) for i in range(1, 11) for j in range(1, 11)}

        # Step #4: Confirm Results
        assert Expected_Results_False_count == results_values_False_count
        assert Expected_Results_Keys == results_keys

    def test_generate_field_dic_type(self):
        '''
        do: Call generate_field and analyis the returned dictionary values (None, False, True)
        logic: Confirm that the current_battlefield dictionary values only contains (None, False, True)
        '''
        # Step 1: Call Function
        results = generate_field()

        # Step #2: Logic to check the contents of the results
        Error_Flag = False
        for i in results.values():
            if i not in (True, False, None):
                Error_Flag = True
                break
            else:
                Error_Flag = False

        # Step#3: Confirm Results
        assert Error_Flag == False

    def test_generate_field_ships(self):
        '''
        do: Call generate_field and checek that the corret number and size of ships is generated
        logic: Confirm that the generated_field contains:
            1. One shipe of length 4.
            2. Two ships of length 3.
            3. Three ships of length 2.
            4. Four ships of length 1.
        '''
        # Step #1: Call Function
        results = generate_field()
        
        # Step #2: Configure (10x10) Field and ship count dic
        rows, cols = 10, 10
        ship_count = {1: 0, 2: 0, 3: 0, 4: 0}
        
        # Step 3: logic to determine ship size and count
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if results.get((i, j)) is False:
                    ship_length = 1                                         # Init Ship Length to 1
                    if j == cols or results.get((i, j + 1)) != False:
                        if i != rows or results.get((i + 1, j)) == False: 
                            # Vertical ship detection
                            for k in range(i + 1, rows + 1):
                                if results.get((k, j)) is False:
                                    ship_length += 1                        # Given cell is False = Ship is taller then expected. Increase Length
                                    results[(k, j)] = True                  # Mark this cell as checked
                                else:
                                    break
                    else:
                        # Horizontal ship detection
                        for k in range(j + 1, cols + 1):
                            if results.get((i, k)) is False:
                                ship_length += 1                            # Given cell is False = Ship is taller then expected. Increase Length
                                results[(i, k)] = True                      # Mark this cell as checked
                            else:
                                break

                    ship_count[ship_length] += 1                            # Update the ship count for the detected ship                    
                    results[(i, j)] = True                                  # Mark the starting cell as checked

        # Step 4: Confirm results
        assert ship_count[1] == 4
        assert ship_count[2] == 3
        assert ship_count[3] == 2
        assert ship_count[4] == 1