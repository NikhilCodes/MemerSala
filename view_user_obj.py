import pickle

with open("db/db.pickle", 'rb') as f:
    obj = pickle.load(f)
print(obj)
