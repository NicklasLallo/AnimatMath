import random as r
from Solver import *
import itertools as it

class Abstracter():

    def __init__(self):

        self.cheat_digits = (["0","1","2","3","4","5","6","7","8","9"], True)
        self.all_chars = (["0","1","2","3","4","5","6","7","8","9","0","+","*","="],True)

        self.structures = [
            [[[0,"*",1],[1,"*",0]],[self.cheat_digits, self.cheat_digits], ["dummy best action"], []],
            [[[0, "+", 1, "*", 2, "+" ,3],[0, "+", 2, "*",1, "+" ,3]], [self.all_chars, self.cheat_digits, self.cheat_digits, self.all_chars], ["dummy best action"], []],
            [[[0, '1', '+', '1', 1], [0, '2', 1]], [([1], True), ([1], True)], [1], []]
                
        ]
        
        self.goals = [
            [[[0, "=", 0]], [self.cheat_digits], ["RETURN"], [1], []]
        ]

    #Takes a sequence and an abstracted sequence and checks if the abstraction can matches the sequence
    def doesMatch(sequence, abstraction, abstractionvariables, allowPartial = False):
        position = 0
        variables = [[]] * len(abstractionvariables)
        ret = True
        for charNr in range(len(abstraction)):
            char = abstraction[charNr]
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
                    if sequence[position] not in whitelist and 1 not in whitelist:
                        ret = False
                        break
                    if not repeating:
                        variables[char].append(sequence[position])
                        position+=1
                    else:
                        while sequence[position] in whitelist or 1 in whitelist:
                            if charNr+1 < len(abstraction) and type(abstraction[charNr+1]) is str and abstraction[charNr+1] == sequence[position]:
                                break
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
                    if breakagain or (position != len(sequence) and (sequence[position]) in whitelist or 1 in whitelist):
                        ret = False
                        if position == len(sequence):
                            ret = allowPartial
                        break
        return (ret and (position == len(sequence)), variables)
    

    #Takes a sequence and a structure and attempts to apply that structure to that sequence.
    #Returns the altered sequence if successful and None otherwise.
    def applyStructureChange(sequence, structure):
        (match, variables) = Abstracter.doesMatch(sequence, structure[0][0], structure[1])
        if match:
            retString = []
            for char in structure[0][1]:
                if type(char) is str:
                    retString.append(char)
                else:
                    retString.append(variables[char])
            return "".join(list(it.chain.from_iterable(retString)))
        return None

    #Takes a sequence and an abstract goal and checks whether the sequence can lead to that goal 
    #Returns the reformated goal if successful and None otherwise
    def checkAbstractGoal(sequence, goal):
        (match, variables) = Abstracter.doesMatch(sequence, goal[0][0], goal[1], True)
        if not match:
            return None
        for variable in variables:
            if variable == []:
                return None
        retString = []
        for char in goal[0][0]:
            if type(char) is str:
                retString.append(char)
            else:
                retString.append(variables[char])
        return "".join(list(it.chain.from_iterable(retString)))

    def judgeGoalRule(abstraction, solver):
        goodMatches = 0
        badMatches = 0
        for sequence in solver.QTable:
            (match, _) = Abstracter.doesMatch(sequence, abstraction[0][0], abstraction[1])
            if not match: 
                continue
            (bestAction, reward) = solver.bestActionAndReward(sequence)
            if bestAction == abstraction[2][0]:
                goodMatches += 1
            else:
                badMatches += 1
        return (goodMatches, badMatches)

    def judgeStructureRule(structure, solver):
        goodMatches = 0
        badMatches = 0
        for (sequence, action) in solver.QTable:
            newSequence = Abstracter.applyStructureChange(sequence, structure)
            if newSequence == None: 
                continue
            (bestAction, reward) = solver.bestActionAndReward(sequence)
            (bestAction2, reward) = solver.bestActionAndReward(newSequence)
            
            if bestAction == None or bestAction2 == None:
                continue

            if bestAction == bestAction2:
                goodMatches += 1
            else:
                badMatches += 1
        return (goodMatches, badMatches)




    def testStructureFormationRule(self, testSequence, solver):
        action, r = solver.bestActionAndReward(testSequence)
        
        for (sequence, bestAction) in solver.QTable:
            (bestAction, reward) = solver.bestActionAndReward(sequence)
            if bestAction != action:
                continue
            startpos = 0
            endpos = -1
            breakagain = False

            while testSequence[startpos] == sequence[startpos]:
                startpos += 1
                if startpos == len(testSequence) or startpos == len(sequence):
                    breakagain = True
                    break

            while testSequence[endpos] == sequence[endpos]:
                endpos -= 1
                if -endpos > len(testSequence) or -endpos > len(sequence):
                    breakagain = True
                    break

            if breakagain or (startpos == 0 and endpos == -1):
                continue

            seqLen = len(sequence)+endpos+1
            tesLen = len(testSequence)+endpos+1

            if sequence[startpos:seqLen] == "" or testSequence[startpos:tesLen] == "":
                continue

            newStructure = [
                [list(it.chain.from_iterable([[0],testSequence[startpos:tesLen],[1]])), list(it.chain.from_iterable([[0],sequence[startpos:seqLen],[1]]))],
                [([1],True),([1],True)],#[(list(set(testSequence[0:startPos])),True),(list(set(testSequence[endPos:-1])),True)],
                [action], []
            ]

            (goodMatches, badMatches) = Abstracter.judgeStructureRule(newStructure, solver)
            #print((goodMatches, badMatches))
            #print(newStructure, flush = True)
            #print(testSequence, flush = True)
            #print(sequence, flush = True)
            if goodMatches > 0 or badMatches > 0:
                print(newStructure, flush = True)

            if badMatches == 0 and goodMatches > 1:
                self.structures.append(newStructure)
                return newStructure

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


class FakeSolver():
    def __init__(self):
        self.QTable = [
            ("1+1=2",1),
            ("2=2",1),
            ("2+2=4",1),
            ("3+3=3",1),
            ("2*(1+1)=4",2),
            ("2*2=4",2),
            ("1+2=3", 1)
        ]

    def bestActionAndReward(self, state):
        return (1, 1)



f = FakeSolver()

a = Abstracter()

print(a.testStructureFormationRule("1+1=2", f))

print()

print(Abstracter.doesMatch("1+1=2", [0, '1', '+', '1', 1], [([1], True), ([1], True)]))
print(Abstracter.doesMatch("2*(1+1)=4", [0, '1', '+', '1', 1], [([1], True), ([1], True)]))

print()


print(Abstracter.applyStructureChange("1+1=2",[[[0, '1', '+', '1', 1], [0, '2', 1]], [([1], True), ([1], True)], [1], []]))

print()

print(Abstracter.checkAbstractGoal("134=", a.goals[0]))
print(Abstracter.checkAbstractGoal("13", a.goals[0]))
print(Abstracter.checkAbstractGoal("=", a.goals[0]))
print(Abstracter.checkAbstractGoal("13=", a.goals[0]))
print(Abstracter.checkAbstractGoal("134=2", a.goals[0]))
print(Abstracter.checkAbstractGoal("134=123", a.goals[0]))
print(Abstracter.checkAbstractGoal("134=1", a.goals[0]))

