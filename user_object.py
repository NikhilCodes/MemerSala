import pickle

obj = dict()

with open("db/db.pickle", 'wb') as f:
    pickle.dump(obj, f)
