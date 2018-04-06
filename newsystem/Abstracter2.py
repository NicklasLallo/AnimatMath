import random as r
from Solver2 import *
import itertools as it
import copy

class Abstracter():

    def __init__(self):

        self.cheat_digits = (True, True, ["0","1","2","3","4","5","6","7","8","9"])
        self.all_chars = (True, True, ["0","1","2","3","4","5","6","7","8","9","0","+","*","="])

        self.structures = [
            [[[2,0,"*",1,3],[2,1,"*",0,3]],[self.cheat_digits, self.cheat_digits, (True, False, [1]), (True, False, [1])], ["dummy best action"], []],
            [[[0, "+", 1, "*", 2, "+" ,3],[0, "+", 2, "*",1, "+" ,3]], [self.all_chars, self.cheat_digits, self.cheat_digits, self.all_chars], ["dummy best action"], []],
            [[[0, '1', '+', '1', 1], [0, '2', 1]], [(True, False, [1]), (True, False, [1])], [1], []],
            [[[0, '1', '*', '2', 1], [0, '2', 1]], [(True, False, [1]), (True, False, [1])], [1], []],
        ]
        
        self.goals = [
            [[[0, "=", 0]], [self.cheat_digits], ["RETURN"], [1], []]
        ]

        self.alreadyFound = {}

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
    
    #Takes:
    #A sequence as a string
    #An abstraction as a list of chars and numbers referencing variables
    #A list of sets of allowed characters for each variable of the form: (repeated, atleastOne, [chars])
    def doesMatch2(sequence, abstraction, variableChars, allowPartial = False):
        variables = [-1]*len(variableChars)
        var = Abstracter.matchChar(sequence, abstraction, variableChars, 0, 0, 0, variables, allowPartial, {})
        if len(var) > 0:
            return (True, var[0])
        else:
            return (False, [])

    def matchChar(sequence, abstraction, variableChars, seqPos, absPos, writing, variables, partial, visited):
        if (seqPos, absPos, writing) in visited:
            if repr(variables) in visited[(seqPos, absPos, writing)]:
                return []
            else:
                visited[(seqPos, absPos, writing)][repr(variables)] = 1
        else:
            visited[(seqPos, absPos, writing)] = {repr(variables) : 1}

        if absPos == len(abstraction) and seqPos == len(sequence):
            return [variables]
        elif absPos == len(abstraction):
            return []
        elif seqPos == len(sequence):
            if type(abstraction[absPos]) is int:
                var = variables[abstraction[absPos]]
                if var != -1 and len(var) > 0 and (writing == -1 or writing == len(var)):
                    absPos += 1

            ret = True
            for pos in range(absPos, len(abstraction)):
                if type(abstraction[pos]) is str:
                    ret = False
                    break
                (repeated, atleastOne, whitelist) = variableChars[abstraction[pos]]
                if not repeated or atleastOne:
                    ret = False
                    break
                if variables[abstraction[pos]] == -1:
                    variables[abstraction[pos]] = []
                elif variables[abstraction[pos]] != []:
                    ret = False
                    break
                 
            if ret or partial:
                return [variables]

            return []
    
        absChar = abstraction[absPos]
        char = sequence[seqPos]
        if type(absChar) is str:
            if char != absChar:
                return []
            return Abstracter.matchChar(sequence, abstraction, variableChars, seqPos+1, absPos+1, 0, variables, partial, visited)
        
        (repeated, atleastOne, whitelist) = variableChars[absChar]

        first = False
        if variables[absChar] == -1:
            variables[absChar] = []
            writing = -1
            first = True

        if writing == -1:

            if first and atleastOne:
                if char not in whitelist and 1 not in whitelist:
                    return []
                variables[absChar].append(sequence[seqPos])
                ret = []
                var = copy.deepcopy(variables)
                ret += Abstracter.matchChar(sequence, abstraction, variableChars, seqPos+1, absPos+1, 0, variables, partial, visited)
                if repeated and seqPos+1 < len(sequence) and (sequence[seqPos+1] in whitelist or 1 in whitelist):
                    ret += Abstracter.matchChar(sequence, abstraction, variableChars, seqPos+1, absPos, -1, var, partial, visited)
                return ret

            if char not in whitelist and 1 not in whitelist:
                return Abstracter.matchChar(sequence, abstraction, variableChars, seqPos, absPos+1, 0, variables, partial, visited)

            ret = []
            var = copy.deepcopy(variables)
            var[absChar].append(char)
            ret += Abstracter.matchChar(sequence, abstraction, variableChars, seqPos, absPos+1, 0, variables, partial, visited)
            ret += Abstracter.matchChar(sequence, abstraction, variableChars, seqPos+1, absPos, -1, var, partial, visited)
            return ret

        if writing == len(variables[absChar]):
            return Abstracter.matchChar(sequence, abstraction, variableChars, seqPos, absPos+1, 0, variables, partial, visited)

        if char != variables[absChar][writing]:
            return []

        return Abstracter.matchChar(sequence, abstraction, variableChars, seqPos+1, absPos, writing+1, variables, partial, visited)

    
    #Takes a sequence and a structure and attempts to apply that structure to that sequence.
    #Returns the altered sequence if successful and None otherwise.
    def applyStructureChange(sequence, structure):
        (match, variables) = Abstracter.doesMatch2(sequence, structure[0][0], structure[1])
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
        (match, variables) = Abstracter.doesMatch2(sequence, goal[0][0], goal[1], True)
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

    #Takes a sequence, an abstract goal, and a solver
    #Returns the abstract goal sequence and the reliability of reaching it if possible, None otherwise
    def advancedCheckAbstractGoal(sequence, goal, solver):
        newSequence = Abstracter.checkAbstractGoal(sequence, goal)
        if newSequence == None:
            return None
        reliability = solver.reliabilityToGoal(sequence, newSequence)
        return (newSequence, reliability)

    def judgeGoalRule(abstraction, solver):
        goodMatches = 0
        badMatches = 0
        for sequence in solver.QTable:
            (match, _) = Abstracter.doesMatch2(sequence, abstraction[0][0], abstraction[1])
            if not match: 
                continue
            (bestAction, reward) = solver.bestActionAndReward(sequence)
            if bestAction == None:
                continue
            if bestAction == abstraction[2][0]:
                goodMatches += 1
            else:
                if abstraction[2][0] in solver.QTable[sequence] and solver.QTable[sequence][bestAction] == reward:
                    goodMatches += 1
                else:
                    badMatches += 1
        return (goodMatches, badMatches)

    def judgeStructureRule(structure, solver):
        goodMatches = 0
        badMatches = 0
        good = []
        for sequence in solver.QTable:
            if len(solver.QTables[sequence]) < 2:
                continue

            newSequence = Abstracter.applyStructureChange(sequence, structure)
            if newSequence == None: 
                continue

            (bestAction, reward) = solver.bestActionAndReward(sequence)
            (bestAction2, reward2) = solver.bestActionAndReward(newSequence)
            
            if bestAction == None or bestAction2 == None:
                continue

            if len(solver.QTable[newSequence]) < 2:
                continue

            if bestAction == bestAction2:
                goodMatches += 1
                good.append(newSequence)
            else:
                if bestAction in solver.QTable[newSequence] and solver.QTable[newSequence][bestAction] == reward2:
                    goodMatches += 1
                    good.append(newSequence)
                elif bestAction2 in solver.QTable[sequence] and solver.QTable[sequence][bestAction2] == reward:
                    goodMatches += 1
                    good.append(newSequence)
                else:
                    badMatches += 1
        if goodMatches > 1 and badMatches == 0:
            print(good)
        return (goodMatches, badMatches)


    def finiteAutomataPatternFinder(sequenceList):
        graph = {}
        for sequence in sequenceList:
            for position in range(len(sequence)):
            
                if position in graph:
                    row = graph[position]
                else:
                    row = {}
                    graph[position] = row

                char = sequence[position]
                if position == len(sequence)-1:
                    nextChar = 0
                else:
                    nextChar = sequence[position+1]

                if char in row:
                    row[char].add((1,nextChar))
                else:
                    row[char] = set([(1,nextChar)])

                if position == 0:
                    row[char].add((0,0))

                if position+1 in graph:
                    nextRow = graph[position+1]
                else:
                    nextRow = {}
                    graph[position+1] = nextRow

                if nextChar in nextRow:
                    nextRow[nextChar].add((0, char))
                else:
                    nextRow[nextChar] = set([(0, char)])

        print(graph)
        print()

        newGraph = {}
        for pos, row in graph.items():
            newRow = {}
            newGraph[pos] = newRow
            for symbol, keySymbols in row.items():
                key = frozenset(keySymbols)
                if key in newRow:
                    newRow[key].add(symbol)
                else:
                    newRow[key] = set([symbol])
    
        print(newGraph)
        print()

        possibleVariables = {}
        for pos, newRow in newGraph.items():
            for connections, characters in newRow.items():
                addVar = True
                for char in characters:
                    if (1, char) not in connections:
                        addVar = False
                        break
                if not addVar:
                    continue
                possibleStartChars = []
                possibleEndChars = []
                #print(connections)
                for (prevOrNext, char) in connections:
                    if char in characters:
                        continue
                    if prevOrNext == 0:
                        possibleStartChars.append(char)
                    else:
                        possibleEndChars.append(char)
                key = frozenset(characters)
                if key in possibleVariables:
                    (start, end) = possibleVariables[key]
                    start += possibleStartChars
                    end += possibleEndChars
                else:
                    possibleVariables[key] = (possibleStartChars, possibleEndChars)
        
        print(possibleVariables)
        print()

        abstractions = []
        for sequence in sequenceList:
            prevChar = 0
            abstraction = []
            for position in range(len(sequence)):
                char = sequence[position]
                matchFound = False
                for chars in possibleVariables:
                    if char not in chars:
                        continue
                    startChar, endChar = possibleVariables[chars]
                    if prevChar not in startChar and prevChar not in chars:
                        continue
                    if position != len(sequence)-1 and sequence[position+1] not in endChar and sequence[position+1] not in chars:
                        continue
                    if len(abstraction) == 0 or abstraction[-1] != chars:
                        abstraction.append(chars)
                    matchFound = True
                    break
                if not matchFound:
                    abstraction.append(char)
                prevChar = char
            if abstraction not in abstractions:
                abstractions.append(abstraction)
                if sequence[1] == "=" or sequence[2] == "=":
                    print(sequence)
                    print(abstraction)

        print(abstractions)

    def probabilityPatternFinder(sequenceList):
        prevProbTable = {}
        nextProbTable = {}
        for sequence in sequenceList:
            for position in range(len(sequence)):
                
                char = sequence[position]
                if position+1 < len(sequence):
                    nextChar = sequence[position+1]
                else:
                    nextChar = 0

                if char in nextProbTable:
                    (nextCharInserts, nextChars) = nextProbTable[char]
                else:
                    nextCharInserts = 0
                    nextChars = {}
                if nextChar in prevProbTable:
                    (prevCharInserts, prevChars) = prevProbTable[nextChar]
                else:
                    prevCharInserts = 0
                    prevChars = {}

                if char in prevChars:
                    prevChars[char] += 1
                else:
                    prevChars[char] = 1
                if nextChar in nextChars:
                    nextChars[nextChar] += 1
                else:
                    nextChars[nextChar] = 1

                nextProbTable[char] = (nextCharInserts+1, nextChars)
                prevProbTable[nextChar] = (prevCharInserts+1, prevChars)
        
        variables = {}
        for char, (inserts, prevChars) in prevProbTable.items():
            key = set()
            for prevChar in prevChars:
                key.add(prevChar)
            key = frozenset(key)
            if key in variables:
                variables[key].append(char)
            else:
                variables[key] = [char]

        print(variables)


    def testStructureFormationRule(self, testSequence, solver):
        bestStructure = None
        bestStructureMatches = 1
        action, r = solver.bestActionAndReward(testSequence)
        
        #For each encountered sequence we shall compare it to the sequence to be tested
        for sequence in solver.QTable:
            
            # if the current sequence has only one point of data go to the next sequence
            if len(solver.QTable[sequence]) < 2:
                continue

            # if the current sequence does not have the same best action as the one we're testing go to the next sequence
            (bestAction, reward) = solver.bestActionAndReward(sequence)
            if bestAction != action:
                continue

            #Find the parts of the sequences that differ
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

            # if the sequences are completely different go to the next sequence
            if breakagain or (startpos == 0 and endpos == -1):
                continue

            # if the part that differ is empty in one of the sequences go to the next sequence
            seqLen = len(sequence)+endpos+1
            tesLen = len(testSequence)+endpos+1
            if sequence[startpos:seqLen] == "" or testSequence[startpos:tesLen] == "":
                continue

            #Form the new rule
            newStructure = [
                [list(it.chain.from_iterable([[0],testSequence[startpos:tesLen],[1]])), list(it.chain.from_iterable([[0],sequence[startpos:seqLen],[1]]))],
                [(True, True, [1]),(True, True, [1])],#[(list(set(testSequence[0:startPos])),True),(list(set(testSequence[endPos:-1])),True)],
                [action], [reward]
            ]

            if repr(newStructure) in self.alreadyFound:
                continue

            #Find how good the rule is by how often it would provide a good/bad match on current dataset
            (goodMatches, badMatches) = Abstracter.judgeStructureRule(newStructure, solver)

            #If the rule has no bad matches and the highest number of good matches so far, keep it
            if badMatches == 0 and goodMatches > bestStructureMatches:
                self.structures.append(newStructure)
                bestStructure = newStructure
                bestStructureMatches = goodMatches
        
        #if bestStructure != None:
        #    f = open("test_data.txt", "w")
        #    f.write(str(Abstracter.judgeStructureRule(bestStructure, solver)))
        #    f.write("\n")
        #    f.write(str(bestStructure))
        #    f.write("\n")
        #    f.write(str(solver.QTable.keys()))
        #    f.write("\n\n")

        #Return a rule with no bad matches and the highest number of good matches found
        if bestStructure != None:
            self.structures.append(bestStructure)
            self.alreadyFound[repr(bestStructure)] = 1
        return bestStructure

    def structureTreeSearch(self, sequence, depth, visitedNodes = {}):
        if sequence in visitedNodes:
            return (None, None, None)
        else:
            visitedNodes[sequence] = 1
    
        bestValue = -9999
        bestGoal = None
        bestGoalSequence = None
        bestSequence = sequence
        for goal in self.goals:
            goalSequence = Abstracter.checkAbstractGoal(sequence, goal)
            if goalSequence != None and goal[3][0] > bestValue:
                bestValue = goal[3][0]
                bestGoal = goal
                bestGoalSequence = goalSequence

        if depth == 0:
            return (bestGoal, bestGoalSequence, bestSequence)

        for structure in self.structures:
            newSequence = Abstracter.applyStructureChange(sequence, structure)
            if newSequence == None:
                continue
            (goal, goalSequence, seq) = self.structureTreeSearch(newSequence, depth-1, visitedNodes)
            if goalSequence != None and goal[3][0] > bestValue:
                bestValue = goal[3][0]
                bestGoal = goal
                bestGoalSequence = goalSequence
                bestSequence = seq

        return (bestGoal, bestGoalSequence, bestSequence)

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
        self.QTable = {
            "1+1=2" : [1,2],
            "2=2" : [1,2],
            "2+2=4" : [1,2],
            "3+3=3" : [1,2],
            "2*(1+1)=4" : [1,2],
            "2*2=4" : [1,2],
            "1+2=3" : [1,2],
            }

    def bestActionAndReward(self, state):
        return (1, 1)



f = FakeSolver()

a = Abstracter()

strs = [
    "1=1",
    "2=2",
    "3=3",
    "22=22",
    "13=13",
    "23=23",
    "32=32",
    "12=12",
    "11=11",
    "33=33",
    "21=21",
    "31=31",
    "123=123",
    "321=321",
    "232=232",
    "213=213",
    "312=312",
    "111=111",
    "113=113",
    "133=133",
    "222=222",
    "331=331",

]

#Abstracter.finiteAutomataPatternFinder(strs)

print()

#Abstracter.matchChar(sequence, abstraction, variableChars, seqPos, absPos, writing, variables, partial, visited)

sequence = "11+11=22"
sequence2 = "111+11=122"
abstraction = [0, 1, "+", 1, "=", 2, 3]
variableChars = [(True, False, [1]), (True, True, ["1","2","3","4","5"]), (True, True, ["1","2","3","4","5"]), (True, False, [1])]

print(Abstracter.matchChar(sequence, abstraction, variableChars, 0, 0, 0, [-1]*len(variableChars), False, {}))
print(Abstracter.matchChar(sequence2, abstraction, variableChars, 0, 0, 0, [-1]*len(variableChars), False, {}))

print()

print(Abstracter.applyStructureChange("1+1=2", a.structures[2]))
print(Abstracter.applyStructureChange("1*2=2", a.structures[0]))
print(Abstracter.checkAbstractGoal("2=", a.goals[0]))

print()

print(a.structureTreeSearch("2*1=", 5))
