def convert(item):
    """
    str or int -> int ot str

    converts a number in [1; 10] inclusive
    to a capital letter from 'A' to 'J' or vice versa
    depending on the type of item

    if input data is incorrect, returns None
    """
    letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J','K']
    try:
        if type(item) == int:                   # if item = int return letter (str)
            return letters[item - 1]
        if type(item) == str:                   # if item = letter (str) return int
            return letters.index(item) + 1
        return None
    except:
        return None


def is_correct_cell(cell):
    """
    (int, int) -> bool

    returns True if cell can be in a dictionary - representation of
    the battlefield
    """
    return cell[0] >= 1 and cell[0] <= 10 and cell[1] >= 1 and cell[1] <= 10        # (X,Y): return True if x and y value are between 1 and 10
