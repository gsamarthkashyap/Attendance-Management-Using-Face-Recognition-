import pickle

with open("encodings.pickle", "rb") as f:
    known_encodings, known_names = pickle.load(f)

print("Names in encoding file:", known_names)
