import pickle

with open("./artifacts/weights.pkl", "rb") as f:
    lmodel_weights = pickle.load(f)
