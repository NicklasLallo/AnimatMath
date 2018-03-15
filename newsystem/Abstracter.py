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

    #Takes a sequence and an abstracted sequence and checks if the abstraction can matches the sequence
    def doesMatch(sequence, abstraction, abstractionvariables, allowPartial = False):
        position = 0
        variables = [[]] * len(abstractionvariables)
        ret = True
        for char in abstraction:
            if position >= len(sequence):
                ret = allowPartial
                break
            if type(char) is str:
                if char != sequence[position]:
                    ret = False
                    break
                position+=1
            else:
                (whitelist, repeating) = abstractionvariables[char]
                if variables[char] == []:
                    variables[char] = []
                    if sequence[position] not in whitelist:
                        ret = False
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
                    breakagain = False
                    for entry in variables[char]:
                        if position >= len(sequence) or entry != sequence[position]:
                            breakagain = True
                            break
                        position += 1
                    if breakagain or (position != len(sequence) and sequence[position]) in whitelist:
                        ret = False
                        if position == len(sequence):
                            ret = allowPartial
                        break
        return (ret and (position == len(sequence)), variables)
    

    #Takes a sequence and a structure and attempts to apply that structure to that sequence.
    #Returns the altered sequence if successful and None otherwise.
    def applyStructureChange(sequence, structure):
        (match, variables) = abstracter.doesMatch(sequence, structure[0][0], structure[1])
        if match:
            retString = []
            for char in structure[0][1]:
                if type(char) is str:
                    retString.append(char)
                else:
                    retString.append(variables[char])
            return list(it.chain.from_iterable(retString))
        return None

    #Takes a sequence and an abstract goal and checks whether the sequence can lead to that goal 
    #Returns the reformated goal if successful and None otherwise
    def checkAbstractGoal(sequence, goal):
        (match, variables) = Abstracter.doesMatch(sequence, goal[0], goal[1], True)
        if not match:
            return None
        for variable in variables:
            if variable == []:
                return None
        retString = []
        for char in goal[0]
            if type(char) is str:
                retString.append(char)
            else:
                retString.append(variables[char])
        return list(it.chain.from_iterable(retString))

    def judgeAbstractGoal():
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

a = Abstracter()
print(Abstracter.checkAbstractGoal("134=", a.goals[0]))
print(Abstracter.checkAbstractGoal("13", a.goals[0]))
print(Abstracter.checkAbstractGoal("=", a.goals[0]))
print(Abstracter.checkAbstractGoal("13=", a.goals[0]))
print(Abstracter.checkAbstractGoal("134=2", a.goals[0]))
print(Abstracter.checkAbstractGoal("134=123", a.goals[0]))
print(Abstracter.checkAbstractGoal("134=1", a.goals[0]))

