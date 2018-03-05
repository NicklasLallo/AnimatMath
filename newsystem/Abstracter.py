import random as r
from Brain import *
import itertools as it

class Abstracter():

    def __init__(self):

        self.cheat_digits = (["0","1","2","3","4","5","6","7","8","9"], True)

        self.structures = [
            [[[0,"*",1],[1,"*",0]],[self.cheat_digits, self.cheat_digits], "dummy best action", []]
                
        ]
        
        self.goals = []


    def applyStructureChange(sequence, structure):
        for match in range(len(structure[0])):
            position = 0
            variables = [[]] * len(structure[1])
            for char in structure[0][match]:
                if position >= len(sequence):
                    break
                if type(char) is str:
                    if char != sequence[position]:
                        break
                    position+=1
                else:
                    (whitelist, repeating) = structure[1][char]
                    if variables[char] == []:
                        variables[char] = []
                        if sequence[position] not in whitelist:
                            break
                        if not repeating:
                            variables[char].apppend(sequence[position])
                            position+=1
                        else:
                            while sequence[position] in whitelist:
                                variables[char].append(sequence[position])
                                position+=1
                                if position >= len(sequence):
                                    break
                    else:
                        breakagain = False
                        for entry in variables[char]:
                            if position >= len(sequence) or entry != sequence[position]:
                                breakagain = True
                                break
                            position += 1
                        if breakagain or sequence[position] in whitelist:
                            break
            output = (match + 1) % 2
            retString = []
            for char in structure[0][output]:
                if type(char) is str:
                    retString.append(char)
                else:
                    retString.append(variables[char])
            return list(it.chain.from_iterable(retString))


abstracter = Abstracter()
print(abstracter.structures[0])
print(Abstracter.applyStructureChange("32*22", abstracter.structures[0]))

