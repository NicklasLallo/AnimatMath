import random as r
from Solver import *
import itertools as it

class Abstracter():

    def __init__(self):

        self.cheat_digits = (["0","1","2","3","4","5","6","7","8","9"], True)
        self.all_chars = (["0","1","2","3","4","5","6","7","8","9","0","+","*","="],True)

        self.structures = [
            [[[0,"*",1],[1,"*",0]],[self.cheat_digits, self.cheat_digits], "dummy best action", []],
            [[[0, "+", 1, "*", 2, "+" ,3],[0, "+", 2, "*",1, "+" ,3]], [self.all_chars, self.cheat_digits, self.cheat_digits, self.all_chars], "dummy best action", []]
                
        ]
        
        self.goals = [
            [[0, "=", 0], [self.cheat_digits], ["RETURN"], [1], []]
        ]

    #Takes a sequence and a structure and attempts to apply that structure to that sequence.
    #Returns the altered sequence if successful and None otherwise.
    def applyStructureChange(sequence, structure):
        for match in range(len(structure[0])):
            position = 0
            variables = [[]] * len(structure[1])
            breakagain = False
            for char in structure[0][match]:
                if position >= len(sequence):
                    breakagain = True
                    break
                if type(char) is str:
                    if char != sequence[position]:
                        breakagain = True
                        break
                    position+=1
                else:
                    (whitelist, repeating) = structure[1][char]
                    if variables[char] == []:
                        variables[char] = []
                        if sequence[position] not in whitelist:
                            breakagain = True
                            break
                        if not repeating:
                            variables[char].append(sequence[position])
                            position+=1
                        else:
                            while sequence[position] in whitelist:
                                variables[char].append(sequence[position])
                                position+=1
                                if position >= len(sequence):
                                    break
                    else:
                        breakagainagain = False
                        for entry in variables[char]:
                            if position >= len(sequence) or entry != sequence[position]:
                                breakagainagain = True
                                break
                            position += 1
                        if breakagainagain or sequence[position] in whitelist:
                            breakagain = True
                            break
            if (not breakagain) and (position == len(sequence)):
                output = (match + 1) % 2
                retString = []
                for char in structure[0][output]:
                    if type(char) is str:
                        retString.append(char)
                    else:
                        retString.append(variables[char])
                return list(it.chain.from_iterable(retString))
            return None

    #Takes a sequence and an abstract goal and checks whether the sequence can lead to that goal 
    #Returns the reformated goal if successful and None otherwise
    def checkAbstractGoal(sequence, goal):
        pass
        

    def fakeMultiplicationTableAbstracter(sequence):
        #if len(sequence) == 1:
        #    return "X"
        #if len(sequence) == 2 and sequence[1] == "*":
        #    return "X*"
        #if len(sequence) == 3 and sequence[1] == "*":
        #    return "X*X"
        if len(sequence) == 4 and sequence[1] == "*" and sequence[3] == "=":
            return "{}=".format(int(sequence[0]) * int(sequence[2]))
        if len(sequence) > 4 and sequence[1] == "*" and sequence[3] == "=":
            return "{}=".format(int(sequence[0]) * int(sequence[2])) + sequence[4:]
        return sequence

    def fakeEqualsAbstracter(sequence):
        if sequence[-1] == "=":
            return sequence + sequence[:-1]
        i = sequence.find("=")
        if i == -1:
            return None
        if len(sequence) > 2*i+1:
            return None
        for x in range(i):
            if len(sequence) <= x+i+1:
                break
            if sequence[x] != sequence[x+i+1]:
                return None
        return sequence[:i] + "=" + sequence[:i]
