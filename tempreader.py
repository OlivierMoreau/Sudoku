import pickle

with open("grids.data", "rb") as f:
    content= pickle.load(f)
    print(content[2000][2],content[2999][2])
