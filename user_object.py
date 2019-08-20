import pickle

obj = {
    "alphanikhil": "shield",
}

with open("db/db.pickle", 'wb') as f:
    pickle.dump(obj, f)
