import pytest
from generate_field.common import convert
from generate_field.common import is_correct_cell
from generate_field.ship_data import has_ship
from generate_field.ship_data import ship_size


class Tests_ship_data:

    ##############################################################################################################
    # has_ship function Tests
    @pytest.mark.parametrize("cell,expected_result", [
            (("D",5), False),     # Valid Input (str,int)
            (("A",1), False),     # Valid Input at boundry edge
            (("A",10), False),    # Valid Input at boundry edge
            (("J",1), False),     # Valid Input within range
            (("J",10), False)     # Valid Input within range
            ])
    def test_has_ship(self,cell,expected_result):
        '''
        do: Generate a 10x10 battlefield with all None and confirm basic functionaliy of has_ship.
        Logic: This test aims to test 5 different cases, including: valid values that are within
        the boundry (1 --> 10, 1--> 10) and valid values that are at the boundry edge (corner cases) 
        -----------------------------
            cell format
                A B C D E F F H I J K
            1
            2
            3
            4
            5
            6
            7
            8
            9
            10
        '''
        # Generate a 10x10 Field, all the field cells are None
        battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}

        result = has_ship(battlefield,cell)
        assert result == expected_result


    @pytest.mark.parametrize("cell", [
        ("Y",5),                            # Invalid Character - Out of Range A --> J 
        ("A",100)                           # Invalid integer - Out of Range 1 --> 10
        ])
    def test_has_ship_key_error(self,cell):
        '''
        do: Generate a 10x10 battlefield with all None and pass arguments that are outside the range
        Logic: This test aims to confirm that if:
            1- A letter out of the defined letters ==> A B C D E F F H I J
            2- Integer out of range (1 --> 10)
        is passed to the function a key error will be raised.
        '''
        # Generate a 10x10 Field, set all the field cells are None
        battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)}   

        with pytest.raises(KeyError):
            has_ship(battlefield,cell)

    ##############################################################################################################
    # has_ship function Tests
    @pytest.mark.parametrize("cell,is_convert,expected_result", [
        ((1,1),False,(4, {(1, 1), (1, 2), (1, 3), (1, 4)})),                      # Valid Input - Set is_convert to False
        ((1,3),False,(4, {(1, 1), (1, 2), (1, 3), (1, 4)})),                      # Valid Input - Set is_convert to False 
        (("A",1),True,(4, {(1, 1), (1, 2), (1, 3), (1, 4)})),                     # Valid Input - Set is_convert to True
        ((10,10),False,(3, {(10, 10), (9, 10), (8, 10)})),                        # Valid Input - Set is_convert to False
        ((9,10),False,(3, {(10, 10), (9, 10), (8, 10)})),                         # Valid Input - Set is_convert to False
        (("K",10),True,(3, {(10, 10), (9, 10), (8, 10)})),                        # Valid Input - Set is_convert to True
        (("C",5),True,(0,0)),                                                     # Valid Input - No Ships at identified cell
        ((5,5),False,(0,0))                                                       # Valid Input - No Ships at identified cell      
        ])
    def test_ship_size(self,cell, is_convert,expected_result):
        '''
        do: Generate a field at which the ships location is identified and use this knowledge to test the ship_size return results
        logic: Generate a 10x10 field then:
            1. Place a ship with length 4 at {(1,1),(1,2),(1,3),(1,4)}
            2. Place a ship with length 3 at {(8,10),(9,10),(10,10)}
        Next, pass cell values that you are sure have ships like (1,1) and check if the function determine it's size and return it's cell locations in a set
        Then, pass cell values that do not have ships and check if the function return (0,0).
        Then, pass cell values that are out of the range of the identifed field (10x10) and determine if the function raise an error or return (0,0)
        -------------------------
            cell format
            A B C D E F F H I J K
            1 x x x x
            2 
            3 
            4 
            5
            6
            7
            8                    x
            9                    x
            10                   x
        '''
        battlefield = {}
        for row in range(1, 11):
            for col in range(1, 11):
                if row == 1 and 1 <= col <= 4:
                    battlefield[(row, col)] = False
                elif row == 8 and col == 10:
                    battlefield[(row, col)] = False
                elif row == 9 and col == 10:
                    battlefield[(row, col)] = False
                elif row == 10 and col == 10:
                    battlefield[(row, col)] = False
                else:
                    battlefield[(row, col)] = None

        result = ship_size(battlefield,cell,is_convert)

        assert result == expected_result

    @pytest.mark.parametrize("battlefield,cell,is_convert", [
        ("Hi",False,"Hello")             # Invalid Input
        ])
    def test_ship_size_type_error(self,battlefield,cell,is_convert):
        '''
        do: Pass arguments of the wrong type to the ship_size function
        logic: Confirm that when the arguments are not 
                dict(tuple(int, int),
                (str, int) or (int, int),
                bool   
        the function will raise a type error
        '''
        with pytest.raises(TypeError):
            ship_size(battlefield,cell,is_convert) 

    @pytest.mark.parametrize("cell,is_convert", [
        ((100,500),False),                   # Invalid Input - Cell value outside the specified field (10 x 10)
        (("Y",500),True)                     # Invalid Input - Cell value outside the specified field (10 x 10)        
        ])
    def test_ship_size_key_error(self,cell, is_convert):
            '''
            do: Pass invalid arguments out of the range and check the ship_size function
            logic: Confirm when the cell value is outside the range a key error will be raised
            '''
            # Generate battle field
            battlefield = {(i, j): None for i in range(1, 11) for j in range(1, 11)} 

            with pytest.raises(KeyError):
                ship_size(battlefield,cell,is_convert) 
