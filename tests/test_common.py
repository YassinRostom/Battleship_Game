import pytest
from generate_field.common import convert
from generate_field.common import is_correct_cell

class Tests_common:

##############################################################################################################
# convert function Tests

    @pytest.mark.parametrize("item,expected_result",[
        ("F",5),            # Valid Input within the range
        ("A",1),            # Valid Input at boundry edge
        ("K",10),           # Valid Input at boundry edge
        (5,"F"),            # Valid Input within the range
        (1,"A"),            # Valid Input at boundry edge
        (10,"K")            # Valid Input at boundry edge
        ])
    def test_convert(self,item,expected_result):
        '''
        do = Test input (str and int) and check the returned (int and str) are correct.
        logic = Input str and int within the range and at the edge of the range. Then, confirm that the returned values are correct.
        '''
        result = convert(item)
        assert result == expected_result

    @pytest.mark.parametrize("item",[
        (111,1),            # Invalid Input - tup
        11,                 # Invalid Input (Out of range)
        "YY"                # Invalid Input letter not avilable in letters list
        ])
    def test_convert_invalid_input(self,item):
        '''
        do = Test Invalid input (str and int) and check the convert function returns None
        logic = Input int values that are out of the range, strings not in letters list and 
        a tuple to confirm that the function return None when the argurments passed to the
        convert function are not an integer that ranges from 1 to 10 or a letter in
        ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J','K'].
        '''
        result = convert(item)
        assert result == None

##############################################################################################################
# ship_size function Tests

    @pytest.mark.parametrize("cell,expected_result", [
            ((3,5),True),    # Valid Input within the range 
            ((1,1),True),    # Valid Input at boundry edge
            ((10,10),True),  # Valid Input at boundry edge
            ((10,1),True),   # Valid Input at boundry edge
            ((0,11),False),  # Invalid Input outside of boundry
            ((1,0),False)    # Invalid Input outside of boundry
            ])
    def test_is_correct_cell(self,cell,expected_result):
        '''
            do: Test input (int, int) and check the bool returned by the is_correct_cell function
            Logic: This test aims to test 6 different cases, including: valid values that are within
            the boundry (1 --> 10, 1--> 10), valid values that are at the boundry edge (corner cases) 
            and invalid values that are outside of the range.
        '''
        result = is_correct_cell(cell)
        assert result == expected_result

    @pytest.mark.parametrize("cell", [
            ("A",5),    # Invalid Input (str,int)
            (1,"1"),    # Invalid Input (int,str)
            ([1,1],"Hi")
            ])
    def test_is_correct_cell_type_error(self,cell):
        '''
            do: Test input non-integer values and check if the function raises a TypeError
            Logic: This test aims to confirm that the is_correct_cell function raises a 
            TypeError when non-integer values are passed as an argument.
        '''
        with pytest.raises(TypeError):
            is_correct_cell(cell)