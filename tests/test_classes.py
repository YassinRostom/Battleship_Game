import pytest
from unittest.mock import patch, MagicMock, call
from classes import Ship
from classes import Field
from classes import Player
from classes import Game
from generate_field.generate_field import generate_field
from generate_field.ship_data import ship_size
from generate_field.common import convert

##############################################################################################################
# Ship Class function Tests
class Tests_Ship:
    
    ##############################################################################################################
    # shoot_at function Tests
    @pytest.mark.parametrize("coordinate,expected_result", [
            ((1,1),[True,False,False,False]),    # Valid Input at boundry edge
            ((1,2),[False,True,False,False])     # Valid Input within the range
            ])  
    def test_shoot_at_horizontal(self,coordinate,expected_result):
        '''
        do: Pass right coordinate that is in the ship and check shoot_at function updated the correct cells that is hit
        logic: Confirm the functionality of the shoot_at function when the right coordinates are passed as arguments
        in this example:
            bow = (1,1)
            horizontal = True
            length = 4
        Therefore on the field it can be presented as 
        ------------------------------------
                    cell format
                1 2 3 4 5 6 7 8 9 10
            1   x x x x            
            2
            3
            4
            5
            6
            7
            8
            9
            10
        -----------------------------------
        The correct cordinates of the ship are (1,1) (1,2) (1,3) (1,4)
        '''
        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = True
        length = 4
        hit = [False,False,False,False]
        my_ship = Ship(bow, horizontal, length, hit)

        # Step #2: Call shoot_at function
        my_ship.shoot_at(coordinate)

        # Step #3: Compare Results
        assert hit == expected_result

    @pytest.mark.parametrize("coordinate,expected_result", [
            ((1,1),[True,False]),    # Valid Input at boundry edge
            ((2,1),[False,True])     # Valid Input within the range
            ])  
    def test_shoot_at_vertical(self,coordinate,expected_result):
        '''
        do: Pass right coordinate that is in the ship and check shoot_at function updated the correct cells that is hit
        logic: Confirm the functionality of the shoot_at function when the right coordinates are passed in this example
            bow = (1,1)
            horizontal = False
            length = 2
        Therefore on the field it can be presented as 
        ------------------------------------
                    cell format
                1 2 3 4 5 6 7 8 9 10
            1   x               
            2   x
            3   
            4   
            5
            6
            7
            8
            9
            10
        -----------------------------------
        The correct cordinates of the ship are (1,1) (2,1)
        '''
        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = False
        length = 4
        hit = [False,False]
        my_ship = Ship(bow, horizontal, length, hit)

        # Step #2: Call shoot_at function
        my_ship.shoot_at(coordinate)

        # Step #3: Compare Results
        assert hit == expected_result

    @pytest.mark.xfail
    @pytest.mark.parametrize("coordinate,expected_result", [
            ((3,3),[False,False,False,False])    # Valid Input within the range 
            ])  
    def test_shoot_at_wrong_coordinate(self,coordinate,expected_result):
        '''
        do: Pass wrong coordinate that is NOT in the ship and check shoot_at function
        logic: Pass the wrong coordinates and check if the function raises an error or at least do not update
        the _hit list
        ***Bug: The function do NOT determine that the passed coordinate is not within the ship and updates _hit with wrong data.
        '''
        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = True
        length = 4
        hit = [False,False,False,False]
        my_ship = Ship(bow, horizontal, length, hit)

        # Step #2: Call shoot_at function
        my_ship.shoot_at(coordinate)

        # Step #3: Compare Results
        assert hit == expected_result

    ##############################################################################################################
    # is_hit function Tests
    @pytest.mark.parametrize("coordinate,expected_result", [
            ((1,1),True),     # Valid Input at boundry edge
            ((1,2),False)     # Valid Input within the range
            ])  
    def test_is_hit(self,coordinate,expected_result):
        '''
        do: Pass right coordinate that is in the ship and check is_hit function return the correct data
        logic: Confirm the functionality of the is_hit function when the right coordinates are passed in this example
            bow = (1,1)
            horizontal = True
            length = 4
            hit = [True,False,True,False] --> [ Injured Cell, Healthy Cell, Injured Cell, Healthy Cell ]
        The correct cordinates of the ship are (1,1) (1,2) (1,3) (1,4)
        '''
        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = True
        length = 4
        hit = [True,False,True,False]
        my_ship = Ship(bow, horizontal, length, hit)

        # Step #2: Call shoot_at function
        result = my_ship.is_hit(coordinate)

        # Step #3: Compare Results
        assert result == expected_result

    @pytest.mark.xfail
    @pytest.mark.parametrize("coordinate,expected_result", [
            ((3,3),None),     # Invalid Input out of range 
            ])  
    def test_is_hit_wrong_coordinate(self,coordinate,expected_result):
        '''
        do: Pass wrong coordinate that is NOT in the ship and check is_hit function RETURN.
        logic: Pass the wrong coordinates and check if the function raises an error or at least do not update the _hit list
        ***Bug: It has been determined that the function do NOT determine that the passed coordinate is not within 
        the ship and updates _hit with wrong data.
        '''
        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = True
        length = 4
        hit = [True,False,True,False]
        my_ship = Ship(bow, horizontal, length, hit)

        # Step #2: Call shoot_at function
        result = my_ship.is_hit(coordinate)

        # Step #3: Compare Results
        assert result == expected_result

    ##############################################################################################################
    # is_dead function Tests
    @pytest.mark.parametrize("hit,expected_result",[
        ([False,False,False,False], False),
        ([True,False,False,False], False),
        ([True,True,False,False], False),
        ([True,True,True,False], False),
        ([True,True,True,True], True)               # Ship is dead                             
    ])
    def test_is_dead(self,hit,expected_result):
        '''
        do: Confirm that the is_dead dunction can identify if the ship is dead or not
        logic: Setup hit to be a ship of length 4 and incrementally change the number of healthy and injured cells
        within the ship to test if the is_dead function can correctly idenitfy if the ship is dead or not. 
        '''

        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = False          
        length = 4
        my_ship = Ship(bow, horizontal, length, hit)

        # Step #2: Call shoot_at function
        result = my_ship.is_dead()
        
        # Step #3: Compare Results
        assert result == expected_result

    @pytest.mark.xfail
    @pytest.mark.parametrize("hit",[
        [False,"Hello",False,"World"],                            
    ])
    def test_is_dead_wrong_data(self,hit,expected_result):
        '''
        do: Setup hit to conatin wrong type (strings) data and test the is_dead function functionality,
        logic: The aim of this test is to determine if the function is able to idenify if is_hit function contain wrong data type
        and raise an error
        ***bug: the function did not raise an error and continued to count the number of False within the hit list
        '''

        # Step #1: Setup Ship instence
        bow = (1,1)
        horizontal = False          
        length = 4
        my_ship = Ship(bow, horizontal, length, hit)
        
        # Step #2: Compare Results
        with pytest.raises(TypeError):
            my_ship.is_dead()


##############################################################################################################
# Field Class function Tests
class Mimic_Field(Field):
    def __init__(self):
        '''
        Mimic a field rather than generating a random field to be able to determine if the function output is 
        correct or wrong.
        Logic: generate a 10 by 10 field
        --------------------------------
            cell format
              1 2 3 4 5 6 7 8 9 10
            1 H I I H   H H   
            2           
            3 H H I     D     
            4           
            5 I I H     H    
            6           
            7 H I       D    
            8           
            9 I H       H    
            10                   M
        '''
        super().__init__()
        ship_4 = Ship((1, 1), True, 4, [False, True, True, False])  # Horizontal ship of length 4 (Healthy, Injured, Injured, Healthy)
        ship_3_1 = Ship((3, 1), True, 3, [False, False, True])      # Horizontal ship of length 3 (Healthy, Healthy, Injured)
        ship_3_2 = Ship((5, 1), True, 3, [True, True, False])       # Horizontal ship of length 3 (Injured, Injured, Healthy)
        ship_2_1 = Ship((7, 1), True, 2, [False, True])             # Horizontal ship of length 2 (Healthy, Injured)
        ship_2_2 = Ship((9, 1), True, 2, [True, False])             # Horizontal ship of length 2 (Injured, Healthy)
        ship_2_3 = Ship((1, 6), True, 2, [False, False])            # Horizontal ship of length 2 (Healthy, Healthy)
        ship_1_1 = Ship((3, 6), False, 1, [True])                   # Ship of length 1 (Dead)
        ship_1_2 = Ship((5, 6), False, 1, [False])                  # Ship of length 1 (Healthy)
        ship_1_3 = Ship((7, 6), False, 1, [True])                   # Ship of length 1 (Dead)
        ship_1_4 = Ship((9, 6), False, 1, [False])                  # Ship of length 1 (Healthy)
        
        self._field = {
            # Ship of length 4
            (1, 1): ship_4, (1, 2): ship_4, (1, 3): ship_4, (1, 4): ship_4,
            # First ship of length 3
            (3, 1): ship_3_1, (3, 2): ship_3_1, (3, 3): ship_3_1,
            # Second ship of length 3
            (5, 1): ship_3_2, (5, 2): ship_3_2, (5, 3): ship_3_2,
            # First ship of length 2
            (7, 1): ship_2_1, (7, 2): ship_2_1,
            # Second ship of length 2
            (9, 1): ship_2_2, (9, 2): ship_2_2,
            # Third ship of length 2
            (1, 6): ship_2_3, (1, 7): ship_2_3,
            # Ships of length 1
            (3, 6): ship_1_1,
            (5, 6): ship_1_2,
            (7, 6): ship_1_3,
            (9, 6): ship_1_4,
            (10, 10): 'M'       # Miss at this cell
        }      

        # Populate the remaing cells with None
        for row in range(1, 11):
            for col in range(1, 11):
                if (row, col) not in self._field:
                    self._field[(row, col)] = None


class Tests_Field:
    # -------------------------------------------------------------------------------------------------------
    # Field Class: _get_field function
    def test_get_field_displayship_True(self):
        '''
        do: Uitilse the Mimic_Field class to test the _get_field function
        logic: Generate a field manually (See Mimic_Field class docstring) that mimics the field which the generate_field() function randomly generates.
        The aim of mimicing a field is to be able to determine the expected_output and compare it to the return of the _get_field function.
        ------------------------------
            cell format
              1 2 3 4 5 6 7 8 9 10
            1 H I I H   H H   
            2           
            3 H H I     D     
            4           
            5 I I H     H    
            6           
            7 H I       D    
            8           
            9 I H       H    
            10                   M
        '''
        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field()

        # Step #2: Set Expected Output
        expected_output = ('HIIH HH   \n          \nHHI  D    \n          \nIIH  H    \n          \nHI   D    \n          \nIH   H    \n         M')
        
        # Step #3: Compare Results
        assert my_field._get_field(True) == expected_output

    @pytest.mark.xfail(reson="untouched cells are still displayed as empty cells not ~")
    def test_get_field_displayship_False(self):
        '''
        do: Uitilse the Mimic_Field class to test the _get_field function
        logic: Similar to the previous test but now set the displayship flag to False.
        ***bug: According to the Field Class in class.py when displayship is False function returns a string with ships in this format:
                'I' - injured cell of the ship
                'D' - dead ship
                'M' - miss
                '~ ' - untouched cell on the field
            However, the untouched cells are still displayed as empty cells not ~
        '''
        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field()

        # Step #2: Set Expected Output
        expected_output = ('~II~~~~~~~\n~~~~~~~~~~\n~~I~~D~~~~\n~~~~~~~~~~\nII~~~~~~~~\n~~~~~~~~~~\n~I~~~D~~~~\n~~~~~~~~~~\nI~~~~~~~~~\n~~~~~~~~~M')
        
        # Step #3: Compare Results
        assert my_field._get_field(False) == expected_output

    def test_get_field(self):
        '''
        do: Test the normal functionality of the _get_field function.
        logic: Confirm that the get_field function randomly generates a field which contains 20 Healthy (H) ships.
        The ships are healthy at this stage becuase the game have not been started yet and the players did not start
        hitting ships
        '''

        # Step #1: Instance class Field        
        my_field = Field()

        # Step #2: Count the number of Healthy ships in the randomly generated field
        result = my_field._get_field(True).count("H") 

        # Step #3: Compare Results 
        expected_result = 20
        assert result == expected_result

    # -------------------------------------------------------------------------------------------------------
    # Field Class: is_hit function
    @pytest.mark.parametrize("coordinate,expected_result", [
            ((1,1),False),      # Healthy Cell 
            ((1,2),True),       # Injured Cell
            ((3,6),True),       # Damaged Ship of Length 1
            ])      
    def test_is_hit(self,coordinate,expected_result):
        '''
        do: Uitilse the Mimic_Field class to test the _is_hit function
        Logic: To pass cells which I now if there is a ship instance in it or not and the condition of the ship.
        Then, compare the return of the is_hit function with the expected results.
        ---------------------------
            cell format
              1 2 3 4 5 6 7 8 9 10
            1 H I I H   H H   
            2           
            3 H H I     D     
            4           
            5 I I H     H    
            6           
            7 H I       D    
            8           
            9 I H       H    
            10                   M  
        '''

        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field()

        # Step #2: Compare Results 
        assert my_field.is_hit(coordinate) == expected_result

    @pytest.mark.xfail    
    @pytest.mark.parametrize("coordinate,expected_result", [
            ((10,10),True),     # Cordinate that is not a ship cell and had a hit which became a "M"
            ((1,2),False),      # Empty cell that is not hit, so expected result is False
            ])      
    def test_is_hit_errors(self,coordinate,expected_result):
        '''
        do: Uitilse the Mimic_Field class to test the _is_hit function
        Logic: Aim is to test unique conditions:
            1. A cell that does not have a ship and is hit. According to the is_hit docstring "returns True if coordinate on the field is hit"
               therefore the expected results is True becuase this cell is hit.
            2. An empty cell that have not been hit, becuase this cell is not hit expected result is False. 
        ***bug: 
            For point 1, The function returns string "M" for (10,10) which is not a bool.
            For point 2, The function returns None which is not a bool.
            ---------------------------
            cell format
              1 2 3 4 5 6 7 8 9 10
            1 H I I H   H H   
            2           
            3 H H I     D     
            4           
            5 I I H     H    
            6           
            7 H I       D    
            8           
            9 I H       H    
            10                   M  
        '''

        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field()

        # Step #2: Compare Results 
        assert my_field.is_hit(coordinate) == expected_result

    @pytest.mark.parametrize("coordinate", [
            (11,11),
            (100,100),
            ])      
    def test_is_hit_outbound_coordinate(self,coordinate):
        '''
        do: Pass coordinate that are outside the 10x10 field.
        Logic: Confirm that the function raise an error when cells outside the field are passed.
        '''

        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field()

        # Step #2: Compare Results 
        with pytest.raises(KeyError):
            my_field.is_hit(coordinate)

    # -------------------------------------------------------------------------------------------------------
    # Field Class: shoot_at function
    
    @pytest.mark.parametrize("coordinate,expected_result__field,expected_result_shoot_at", [
            ((9,9),True,False)     # Cordinate that is not a ship cell and has not been hit before
             ]) 
    def test_shoot_at_Empty_Cell(self,coordinate,expected_result__field,expected_result_shoot_at):
        '''
        do: pass an argument that have no ship cells and has not been hit previously.
        logic: confirm that shoot_at return False and update the _field with True to indicate that this cell is hit now.
        '''
        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field() 
        result = my_field.shoot_at(coordinate)

        # Step #2: Compare Results
        assert my_field._field[coordinate] == expected_result__field
        assert result == expected_result_shoot_at

    @pytest.mark.parametrize("coordinate,expected_result__field,expected_result_shoot_at", [
            ((1,1),[True, True, True, False],True),
            ((3,3),[False, False, True],True)
             ])
    def test_shoot_at_cell_has_ship(self,coordinate,expected_result__field,expected_result_shoot_at):
        '''
        do: pass an argument that have a healthy ship
        logic: To pass coordinate that contains a healthy ship and confirm that the ship objects (_hit) are
        updated correctly, shoot_at function returns False and number of cell left is decreased by 1.
        The secod paramter run the same test but pass an cordinate that have an injured ship cell.
        '''
        # Step #1: Instance class Mimic_Field and call shoot_at function
        my_field = Mimic_Field() 
        initial_ships_left = my_field.cells_left    # Get value of cells left before hitting a new cell
        result = my_field.shoot_at(coordinate)

        # Step #3: Compare Results
        assert my_field._field[coordinate]._hit == expected_result__field
        assert result == expected_result_shoot_at
        assert my_field.cells_left == initial_ships_left - 1


    @pytest.mark.xfail
    @pytest.mark.parametrize("coordinate,expected_result__field,expected_result_shoot_at", [
            ((1,1),[True, True, True, False],True)
              ]) 
    def test_shoot_at_cell_cells_left(self,coordinate,expected_result__field,expected_result_shoot_at):
        '''
        do: pass an argument that have a healthy ship, then recall the same function using the exact same cordinate
        logic: To call the shoot_at function to hit coordinate (1,1) and then re-call the function to hit the same
        coordinate and detrmine if the number of ships left is affected (after 2nd hit) or not.
        ***bug: the function did modify the cells_left twice eventhough the shoot_at function targeted the same cordinate.
        The function failed to idenitfy that it already shoot at this cordinate before.
        '''
         # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field() 
        initial_ships_left = my_field.cells_left    # Get value of cells left before hitting a new cell
        
        # Step #2: Function Call # 1
        result = my_field.shoot_at(coordinate)        

        # Step #3: Function Call # 2
        result = my_field.shoot_at(coordinate)        

        # Step #4: Compare Results
        assert my_field._field[coordinate]._hit == expected_result__field
        assert result == expected_result_shoot_at
        assert my_field.cells_left == initial_ships_left - 1


    @pytest.mark.parametrize("coordinate", [
            (11,11),
            (100,100),
            ])      
    def test_shoot_at_outbound_coordinate(self,coordinate):
        '''
        do: Pass coordinate that are outside the 10x10 field.
        Logic: Confirm that the function raise an error when cells outside the field are passed.
        '''

        # Step #1: Instance class Mimic_Field
        my_field = Mimic_Field()
        
        # Step #2: Compare Results
        with pytest.raises(KeyError):
            my_field.shoot_at(coordinate)


##############################################################################################################
# Player Class function Tests

class Tests_Player:

    @patch('builtins.input', return_value='John')
    def test_player_initialization(self, mock_input):
        '''
        do: init a player name
        Logic: generate an instance of class Player and check the attribute name
        '''
        player = Player(1)
        assert player._name == 'John'

    @patch('builtins.input', side_effect=['Yas','A4','A4','X100','ASDASD', 'B5'])
    def test_read_position(self, mock_input):
        '''
        do: Mimic the user input for the player name and position
        logic: Confirm that the read_position function returns the correct value (line, row) when the user input valid positions and 
        does not return any data when the user inputs are invalid (X100,ASDASD) or the user have inputed the same position twice.
        Sequence of Operation:
        ----------------------
            1. User Input - Name --> Yas
            2. User Input - Position -> A4
            3. User Input - Position -> A4
            4. User Input - Position -> X100
            5. User Input - Position -> ASDASD
            6. User Input - Position -> B5
        '''
        # Step #1: Instance classes
        player = Player(1)
        opponent_field = MagicMock()

        # Step #2: Setup MagicMock returns
        opponent_field.is_hit = MagicMock(side_effect=[False, True, False, False, False])

        # Step #3:  Compare Results
        position = player.read_position(opponent_field)
        assert position == (4, 1)  # A4 converted to (4, 1)

        position = player.read_position(opponent_field)
        assert position == (5, 2)  # B5 converted to (5, 2)


##############################################################################################################
# Game Class function Tests

class Mimic_Game(Game):
    def __init__(self):
        '''
        Mimic_Game inherit the properties and methods of the Game class. Additionally, the _fields attribute 
        is overridden to use Mimic_Field instances instead of Field instances.
        '''
        super().__init__()
        self._fields = [Mimic_Field(), Mimic_Field()]

# Mock class for Field
class Field_Cells(Field):
    '''
        Field_Cells inherit the properties and methods of the Field class. Additionally, it overrides
        the number of cells_left to help test the is_winner function.
    '''
    def __init__(self, cells_left):
        super().__init__()
        self.cells_left = cells_left

class Tests_Game:

    # -------------------------------------------------------------------------------------------------------
    # Game Class: increase_player function
    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_increase_player(self, mock_input):
        '''
        do: Create an instance of class Game and set Player 1 Name = Andy and Player 2 Name = Tom
        logic: After creating an instance of class Game and setting Player 1 and 2 names. Confirm the initial
        value of the attribute _current_player.
        Then call the increase_player function and confirm that the _current_player attribute has been updated.
        '''

        # Step #1: Create an Instance of class Game
        game = Game()
        
        # Step #2: confirm _current_player is 1
        assert game._current_player == 1
        assert game.get_index() == 0
        
        # Step #3: Call increase_player function and confirm _current_player is 2 now
        game.increase_player()
        assert game._current_player == 2
        
        # Step #4: Call increase_player function and confirm _current_player is 1 again
        game.increase_player()
        assert game._current_player == 1


    # -------------------------------------------------------------------------------------------------------
    # Game Class: get_index and get_opponent_index function
    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_get_index_get_opponent_index(self, mock_input):
        '''
        do: Create an instance of class Game and set Player 1 Name = Andy and Player 2 Name = Tom
        logic: After creating an instance of class Game and setting Player 1 and 2 names. 
            1. Check the get_index and get_opponent_index functions returns stright after creating a Game instance and setting the Player names.
            2. Call the increase_player function and check the get_index and get_opponent_index functions returns.
            3. Re-Call the increase_player function and check the get_index and get_opponent_index functions return again.
        '''

        # Step #1: Create an Instance of class Game
        game = Game()
        
        # Step #2: confirm _current_player is 1
        assert game.get_index() == 0
        assert game.get_opponent_index() == 1
        
        # Step #3: Call increase_player function
        game.increase_player()
        assert game.get_index() == 1
        assert game.get_opponent_index() == 0
        
        # Step #4: Re-Call increase_player function
        game.increase_player()
        assert game.get_index() == 0
        assert game.get_opponent_index() == 1

    # -------------------------------------------------------------------------------------------------------
    # Game Class: field_with_ships and field_without_ships function
    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_field_with_ships(self, mock_input):
        '''
        do: Use the field_with_ships and field_without_ships functions to check the content of the fields.
        logic: At this stage of the game, the field for each player has just been created therefore their should be 
        20 cells with Healthy ships and no hits at all.
            1. Confirm the field_with_ships conatins 20 Healthy Ships
            2. Confirm the field_without_ships contains 0 Healthy ships [At this stage, no ship hit took place yet] 
        '''

        # Step #1: Create an Instance of class Game and call functions
        game = Game()
        Player_1_field_with_ships = game.field_with_ships(0)
        Player_1_field_without_ships = game.field_without_ships(0)

        # Step #2: Determine the results
        Player_1_Healthy_Ships = Player_1_field_with_ships.count("H")
        Player_1_Healthy_Ships_field_without_ships = Player_1_field_without_ships.count("H")

        # Step #3: Confirm results
        assert Player_1_Healthy_Ships == 20
        assert Player_1_Healthy_Ships_field_without_ships == 0

    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_field_with_ships_advanced(self, mock_input):
        '''
        do: Use Mimic_Game class to test the return of the field_with_ships and field_without_ships function
        logic: The Mimic_Game is used to represent a more advance stage of the game were some ships have been hit.
            1. Confirm the field_with_ships conatins H, I, D and M
            2. Confirm the field_without_ships contains No H
        --------------------------------
            cell format
              1 2 3 4 5 6 7 8 9 10
            1 H I I H   H H   
            2           
            3 H H I     D     
            4           
            5 I I H     H    
            6           
            7 H I       D    
            8           
            9 I H       H    
            10                   M
        '''

        # Step #1: Create an Instance of class Mimic_Game and call functions
        game = Mimic_Game()
        Player_1_field_with_ships = game.field_with_ships(0)
        Player_1_field_without_ships = game.field_without_ships(0)

        # Step #2: Confirm results
        assert Player_1_field_with_ships == 'HIIH HH   \n          \nHHI  D    \n          \nIIH  H    \n          \nHI   D    \n          \nIH   H    \n         M'
        assert Player_1_field_without_ships == ' II       \n          \n  I  D    \n          \nII        \n          \n I   D    \n          \nI         \n         M'


    # -------------------------------------------------------------------------------------------------------
    # Game Class: is_winner function
    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_is_winner(self, mock_input):
        '''
        do: Confirm that the is_winner function is able to identify the winner based on the number of cells_left in field.
        logic: create a Field_Cells class that inherits the Field Class functionality and override the cells_left value
        to be able to test different conditions for the is_winner function.
            1. Test 1: Player 1 have no cells_left. Therefore Player_2 is Winner.
            2. Test 2: Player 2 have no cells_left. Therefore Player_1 is Winner.
            3. Test 3: Player 1 and 2 have cells_left. Therefore No Winner yet.
        '''
        # Step #1: Create an Instance of class Game
        game = Game()
        
        # Step #2: call functiona nd compare results
        game._fields = [Field_Cells(0), Field_Cells(1)]  # Player 1's field has 0 cells left
        assert game.is_winner() == 2                     # Winner: Player 2

        game._fields = [Field_Cells(1), Field_Cells(0)]  # Player 2's field has 0 cells left
        assert game.is_winner() == 1                     # Winner:  Player 1

        game._fields = [Field_Cells(1), Field_Cells(1)]  # Both fields have cells left
        assert game.is_winner() == False                 # No Winner Yet

    @pytest.mark.xfail
    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_is_winner_error(self, mock_input):
        '''
        do: Test a special case were both players have 0 cells_left.
        logic: create a Field_Cells class that inherits the Field Class functionality and override the cells_left value
        to set them to zero.
        ***Bug: When both players have 0 cells_left. The Game identify Player 2 as the winner eventhough 
        it should be a tie.
        '''
        # Step #1: Create an Instance of class Game
        game = Game()
        
        # Step #2: Compare Results
        game._fields = [Field_Cells(0), Field_Cells(0)]     # Player 1 and 2 fields hve 0 cells left
        assert game.is_winner() == None                     # Expecting a Tie

##############################################################################################################
# Game Class - Start function Tests
class Mimic_Field_2(Field):
    def __init__(self, cells_left):
        '''
        Mimic a field rather than generating a random field to be able to determine if the function output is correct or wrong.
        Logic: generate a 10 by 10 field
        --------------------------------
            cell format
              1 2 3 4 5 6 7 8 9 10
            1 H H   
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
        super().__init__()
        self.cells_left = cells_left

        # Horizontal ship of length 2 (Healthy, Healthy)
        ship_2 = Ship((1, 1), True, 4, [False, False])          
        self._field = {(1, 1): ship_2, (1, 2): ship_2}      

        # Set all remaining cells to None
        for row in range(1, 11):
            for col in range(1, 11):
                if (row, col) not in self._field:
                    self._field[(row, col)] = None

class Tests_Game_Start:
    @patch('builtins.input', side_effect=['Andy','Tom'])
    def test_start(self, mock_input):
        '''
        do: Test the start function functionality when a Player has won the Game.
        logic: Uitilse Field_Cells to set the _fields attribute to indicate that Player 1 (Andy) has no ships left
        which means Andy Lost and Player 2 (Tom) won. Then, confirm the start function prints "Tom won"
        '''
        # Step #1: Create an Instance of class Game set attribute _fields
        game = Game()
        game._fields = [Field_Cells(0), Field_Cells(1)] # Player 2 (Tom) wins

        # Step #2: Call start method and compare results
        with patch('builtins.print') as mock_print:
            game.start()

            expected_call = call("Tom won")
            mock_print.assert_has_calls([expected_call])  # Verify that the print statement was called

    @patch('builtins.input', side_effect=['Andy','Tom',"A1"])
    def test_start_turns(self, mock_input):
        '''
        do: Call game.start() and pass arguments Player 1 name (Andy), Player 2 name (Tom) and Position (A1)
        logic: Mimic_Field_2 is created to inheirt the Field class method and create a bespoke field tht can 
        be used to test the start function prints. 
            In the Mimic_Field_2 the number of cells_left for both players have been set to 1. Also, a field
            was manually created to enable the testing of the prints within the start function.
            This test confirms:
                1. The os.system('clear') was called.
                2. The print statements were called in the correct order and the printed data were correct.
        '''
        # Step #1: Call the Game Instance
        game = Game()

        # Step #2: Set the Game class _fields attribute to Mimic_Field_2(1)
        game._fields = [Mimic_Field_2(1), Mimic_Field_2(1)]


        with patch('os.system') as mock_os_system, patch('builtins.print') as mock_print:
            
            # Step #3: Call the start function
            game.start()

            # Step #3: Check that os.system('clear') was called
            mock_os_system.assert_called_with('clear')

            # Expected sequence of print statements
            expected_calls = [
                call("Andy make your move"),
                call("your field"),
                call('HH        \n          \n          \n          \n          \n          \n          \n          \n          \n          '),  # Mocked field with ships
                call("opponent field"),
                call('          \n          \n          \n          \n          \n          \n          \n          \n          \n          '),  # Mocked opponent field without ships
                call("Andy won")
            ]

            # Step #4: Check that print statements were called in the correct order
            mock_print.assert_has_calls(expected_calls, any_order=False)

