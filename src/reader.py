import pickle

def grid_picker(g, r):
    'pick a grid from the file, g = the grid, r = one of 4 90° rotations'
    with open("./data/grids.data", "rb") as f:
        content= pickle.load(f)
        grid_ret = content[g][0][r]
        full_grid_ret = content[g][1][r]

        return [grid_ret, full_grid_ret]
