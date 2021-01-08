
import pickle

class Reader(object):
    def __init__(self, grid, rotation):
        self.grid = grid
        self.rotation = rotation

    def grid_picker(self):
        'pick a grid from the file, g = the grid, r = one of 4 90° rotations'
        with open("data/grids.data", "rb") as f:
            content= pickle.load(f)
            grid_ret = content[self.grid][0][self.rotation]
            full_grid_ret = content[self.grid][1][self.rotation]

            return [grid_ret, full_grid_ret]
