class Block(object):
    """Abstract class for block objects Rows, Columns & Squares."""

    def __init__(self):
        self.cells = []

    def get_values(self):
        """returns the values of the cells in the block"""
        values = []
        for cell in self.cells:
            values.append(cell.value)
        return values

    # Checks if the input isn't alreay present in this block.
    def check_valid(self, input):
        # This function is only used during auto solving, so users inputs are reseted back to nothing
        for cell in self.cells:
            if cell.state["user_input"]:
                cell.state["user_input"] = False
                cell.value = 0
        if input in self.get_values():
            return False
        else:
            return True


class Row(Block):
    pass


class Column(Block):
    pass


class Square(Block):
    pass
