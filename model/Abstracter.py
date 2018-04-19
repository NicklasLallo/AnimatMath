import random as r
from Solver import *
import itertools as it
import copy

class Abstracter():

    def __init__(self):

        self.cheat_digits = (True, True, ["0","1","2","3","4","5","6","7","8","9"])
        self.all_chars = (True, True, ["0","1","2","3","4","5","6","7","8","9","0","+","*","="])

        self.structures = [
            [[[2,0,"+",1,3],[2,1,"+",0,3]],[self.cheat_digits, self.cheat_digits, (True, False, [1]), (True, False, [1])], ["dummy best action"], []],
            [[[0, "+", 1, "*", 2, "+" ,3],[0, "+", 2, "*",1, "+" ,3]], [self.all_chars, self.cheat_digits, self.cheat_digits, self.all_chars], ["dummy best action"], []],
            [[[0, '1', '+', '1', 1], [0, '2', 1]], [(True, False, [1]), (True, False, [1])], [1], []],
            [[[0, '1', '+', '2', 1], [0, '2', 1]], [(True, False, [1]), (True, False, [1])], [1], []],
        ]
        
        self.goals = [
            #[[[0, "=", 0]], [self.cheat_digits], ["RETURN"], [1], []]
        ]

        self.alreadyFound = {}

    
    #Takes:
    #A sequence as a string
    #An abstraction as a list of chars and numbers referencing variables
    #A list of sets of allowed characters for each variable of the form: (repeated, atleastOne, [chars])
    def doesMatch(sequence, abstraction, variableChars, allowPartial = False):
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
    def applyStructureChange(sequence, structure, returnVariables = False):
        (match, variables) = Abstracter.doesMatch(sequence, structure[0][0], structure[1])
        if match:
            retString = []
            for char in structure[0][1]:
                if type(char) is str:
                    retString.append(char)
                else:
                    retString.append(variables[char])
            if returnVariables:
                return ("".join(list(it.chain.from_iterable(retString))), variables)
            return "".join(list(it.chain.from_iterable(retString)))
        if returnVariables:
            return (None, None)
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
            (match, _) = Abstracter.doesMatch(sequence, abstraction[0][0], abstraction[1])
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


    def equalityJudge(structure, solver):
        goodMatches = 0
        badMatches = 0
        for sequence in solver.inputSet:
            continueagain = False
            branch = solver.rewardedSequencesForward
            for char in sequence:
                if char not in branch.connections:
                    continueagain = True
                    break
                branch = branch.connections[char]
            if continueagain:
                continue

            newSequence = Abstracter.applyStructureChange(sequence, structure)
            if newSequence == None:
                continue

            twig = solver.rewardedSequencesForward
            for char in newSequence:
                if char not in twig.connections:
                    continueagain = True
                    break
                twig = twig.connections[char]
            if continueagain:
                continue

            queue = [(branch, twig)]
            while len(queue) > 0:
                (branch, twig) = queue.pop()
                if branch.node != twig.node:
                    badMatches += 1
                    return (goodMatches, badMatches)
                for char in branch.connections:
                    if char not in twig.connections:
                        badMatches += 1
                        return (goodMatches, badMatches)
                    queue.append((branch.connections[char], twig.connections[char]))
            goodMatches += 1
        return (goodMatches, badMatches)



    def equalityFinder(self, sequence, solver, leastGoodMatches = 4, debug = False):
        (sequences, split) = solver.findClosestRewardedSequences(sequence)
        equality = sequence[:-split]
        equalities = map(lambda x: x[:-split], sequences)
        structs = []
        if debug:
            print(sequence)
            print(sequences)
            print(equalities)

        for equal in equalities:
            first = list(equality)
            first.insert(0,0)
            first.append(1)
            second = list(equal)
            second.insert(0,0)
            second.append(1)

            #Form the new rule
            newStructure = [
                [first, second],
                [(True, False, [1]),(True, False, [1])],
                [], []
            ]

            if repr(newStructure) in self.alreadyFound:
                continue

            (goodMatches, badMatches) = Abstracter.equalityJudge(newStructure, solver)
            if debug:
                print((goodMatches, badMatches))

            if goodMatches < leastGoodMatches and badMatches != 0:
                continue
            if debug:
                print(newStructure)
            self.structures.append(newStructure)
            structs.append(newStructure)
            self.alreadyFound[repr(newStructure)] = 1
        return structs

    def structureTreeSearch(self, sequence, depth, visitedNodes = set(), solver = None, returnImmediately = 9999999, debug = False):
        if sequence == None or sequence in visitedNodes:
            return (None, None, None, None, None, None)
        else:
            visitedNodes.add(sequence)
    
        bestValue = -9999
        bestGoal = None
        bestGoalSequence = None
        bestSequence = None
        bestStructures = None
        bestAction= None
    
        if solver != None:
            (answer, branch) = solver.sequenceInRewarded(sequence)
            if answer:
                seq = [sequence]
                queue = [(branch, seq)]
                while len(queue) > 0:
                    (branch, seq) = queue.pop()
                    if branch.node != None and branch.node[1] != None and branch.node[1] > bestValue:
                        bestValue = branch.node[1]
                        bestGoal = None
                        bestGoalSequence = "".join(seq)
                        bestSequence = sequence
                        bestStructures = []
                        bestAction = branch.node[0]
                        if bestValue > returnImmediately:
                            break
                    for char in branch.connections:
                        nextSeq = list(seq)
                        nextSeq.append(char)
                        queue.append((branch.connections[char], nextSeq))
        
        for goal in self.goals:
            goalSequence = Abstracter.checkAbstractGoal(sequence, goal)
            if goalSequence != None and goal[3][0] != None and goal[3][0] > bestValue:
                bestValue = goal[3][0]
                bestGoal = goal
                bestGoalSequence = goalSequence
                bestStructures = []
                bestAction = goal[2][0]
                if bestValue > returnImmediately:
                    break

        if depth == 0 or bestValue > returnImmediately:
            return (bestGoal, bestGoalSequence, bestSequence, bestStructures, bestAction, bestValue)

        for structure in self.structures:
            newSequence = Abstracter.applyStructureChange(sequence, structure)
            if newSequence == None or len(newSequence) > len(sequence):
                continue
            #if debug:
            #    print(newSequence)
            (goal, goalSeq, seq, structs, action, value) = self.structureTreeSearch(newSequence, depth-1, visitedNodes, solver, returnImmediately, debug)
            if debug and seq != None:
                print(seq)
            if goalSeq != None and value != None and value > bestValue:
                bestValue = value
                bestGoal = goal
                bestGoalSequence = goalSeq
                bestSequence = seq
                bestAction = action
                bestStructures = structs
                bestStructures.insert(0, structure)
                if bestValue > returnImmediately:
                    break

        return (bestGoal, bestGoalSequence, bestSequence, bestStructures, bestAction, bestValue) 
