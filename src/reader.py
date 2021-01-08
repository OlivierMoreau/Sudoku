import pickle

class Reader():

    def __init__(self):
        with open("./data/grids.data", "rb") as f:
            self.content = pickle.load(f)

    def grid_picker(self, g, r):
        'pick a grid from the file, g = the grid, r = one of 4 90° rotations'


        grid_ret = self.content[g][0][r]
        full_grid_ret = self.content[g][1][r]

        return [grid_ret, full_grid_ret]

    def size(self):
        return len(self.content)
