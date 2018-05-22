import pickle
import os.path
import importer
import random

repetitions = 90

favs = [0.1, 0.5, 0.9, 0.1, 0.5, 0.9, 0.1, 0.5, 0.9, 0.1, 0.5, 0.9]
trainingFileNames = ["arithmetic2.dat", "arithmetic2.dat", "arithmetic2.dat", "arithmetic1.dat", "arithmetic1.dat", "arithmetic1.dat", "grammar1.dat", "grammar1.dat", "grammar1.dat", "logic1.dat", "logic1.dat", "logic1.dat"] 
answer_maxlens = [3,3,3,3,3,3,1,1,1,1,1,1]

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


if not os.path.exists("random_data.pkl"):
    data = {}
    save_obj(data, "random_data")
else:
    data = load_obj("random_data")


for x in range(len(favs)):
    if (favs[x], answer_maxlens[x], trainingFileNames[x]) not in data:
        data[(favs[x], answer_maxlens[x], trainingFileNames[x])] = []
    for y in range(repetitions):
        (trainingSet, validSet, chars, action_list, id_to_word) = importer.importData(trainingFileNames[x], None, favs[x])
        info = trainingFileNames[x] + "_" + str(favs[x]) + "_" + str(answer_maxlens[x])
        xs = [0]
        y = 0
        for (seq, out) in validSet:
            s = ""
            for g in range(answer_maxlens[x]):
                symbol = random.choice(action_list)
                if symbol == "RETURN":
                    break
                s = s + symbol
            if s == out:
                y += 1
        y /= len(validSet)
        ys = [y]

        data[(favs[x], answer_maxlens[x], trainingFileNames[x])].append((xs, ys, info)) 
        save_obj(data, "random_data")
