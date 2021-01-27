class Block(object):
    """Abstract class for block objects Rows, Collumns & Squares."""

    def __init__(self):
        self.cells = []

    def get_values(self):
        """returns the values of the cells in the block"""
        values = []
        for cell in self.cells:
            values.append(cell.value)
        return values

    def check_valid(self, val):
        """Checks if user inputs isn't already present in block"""
        for cell in self.cells:
            if cell.state["user_input"]:
                cell.state["user_input"] = False
                cell.value = 0
        if val in self.get_values():
            return False
        else:
            return True


class Row(Block):
    pass


class Collumn(Block):
    pass


class Square(Block):
    pass
