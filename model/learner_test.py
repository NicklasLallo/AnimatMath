from Solver import *
from Abstracter import *

import random as r
import math as m
import plotter

trainingFileName = "arithmetic2.dat"    #The file containing the training data
validFileName = None                    #The file containing the validation set, if None the validation data will be drawn as a fraction of the training data
fraction_as_validation = 0.1            #The fraction of the training data that will be taken for validation, only used if validFileName is None

babble_iterations = 1           #How many iterations the system will be trained on what its actions does
imitation_iterations = 5      #How many iterations the system will be trained on what output is good
abstract_after_iteration = 1    #After how many imitation iterations will the system begin to make equality abstractions
random_order = False            #Whether or not the data will be randomly drawn from the dataset

explore_rate = 0.01     #When training and not imitating, how often will the system make a random move
solver_depth = 4        #How deep will the tree-search of the solver go
abstracter_depth = 1    #How deep will the tree-search of the abstracter go
answer_maxlen = 4       #How many actions can the system make before being forced to return
learning_rate = 0.9     #Learning rate of the system
discount_rate = 0.9     #Discount rate of the system
action_list = ["1","2","3","4","5","6","7","8","9","0","RETURN"]    #List of actions the system can take, can be changed by importData()

info = "DataSet: {}\nFraction used for validation: {}\nBabble iterations: {}\nSolver depth: {}\nAbstracter depth: {}".format(trainingFileName[:-4], fraction_as_validation, babble_iterations, solver_depth, abstracter_depth)
short_info = "{}_{}_{}_{}_{}".format(trainingFileName[:-4], fraction_as_validation, babble_iterations, solver_depth, abstracter_depth)
def importData(trainingFileName, validFileName = None):
    trainingFile = open(trainingFileName, "r")
    trainingSet = []
    splitChar = " "
    lines = trainingFile.readlines()
    lines = list(map(lambda x: x[:-1], lines))
    trainingFile.close()
    header = lines.pop(0)

    splitCharPos = header.find("splitChar:")
    if splitCharPos != -1 and splitCharPos+10 < len(header):
        splitChar = header[splitCharPos+10]
    
    actionListPos = header.find("actionList:")
    if actionListPos != -1:
        actionList = ["RETURN"]
        pos = 11+actionListPos
        while pos < len(header) and header[pos] != splitChar:
            actionList.append(header[pos])
            pos += 1

    for line in lines:
        i = line.index(splitChar)
        trainingSet.append((line[:i], line[i+1:]))
    
    validSet = []
    if validFileName != None:
        validFile = open(validFileName, "r")
        for line in validFile:
            i = line.index(splitChar)
            validSet.append((line[:i], line[i+1:]))
        validFile.close()
    else:
        for n in range(m.ceil(len(trainingSet)*fraction_as_validation)):
            i = r.randrange(0, len(trainingSet))
            validSet.append(trainingSet.pop(i))

    return (trainingSet, validSet)

def abstractSequenceAndGoal(sequence, debug = False):
    (goalRule, goal, newSequence, structs, action, value) = abstracter.structureTreeSearch(sequence, abstracter_depth, solver = solver, returnImmediately = 0.9, debug = debug, visitedNodes = set())
    if debug:
        print((newSequence, goal, action, value))
    if newSequence == None:
        return (sequence, {}, structs)
    return (newSequence, {goal: (action, value)}, structs)

def run_model(sequence, expected_output,  maxlen = 4, training = False, imitation = False, debug = False):
    if imitation:
        expr = sequence + expected_output
    else:
        expr = sequence
    
    (absExpr, absGoal, structs) = abstractSequenceAndGoal(expr)

    if imitation:
        solver.improvedProgram(expr+"D", 0, absExpr+"D", 1, "RETURN", 1, {})
        return expr

    exploreProb = 0
    if training:
        exploreProb = explore_rate

    action = None
    reward = None

    for loop in range(maxlen):
        if not training:
            action = None
            reward = None
        action = solver.improvedProgram(expr, solver_depth, absExpr, exploreProb, action, reward, absGoal, training = training)
        if action == "RETURN":
            reward = -1
            if expr == sequence + expected_output:
                reward = 1
                if debug and absGoal != {}:
                    print(structs)
            if not training:
                action = None
                reward = None
            solver.improvedProgram(expr+"D", 0, absExpr+"D", 1, action, reward, {}, training = training)
            return expr
        reward = 0
        expr += action
        (absExpr, absGoal, structs) = abstractSequenceAndGoal(expr)
    if debug:
        return (expr, structs)
    return expr



(trainingSet, validSet) = importData(trainingFileName, validFileName)

solver = Solver(action_list, learning_rate, discount_rate)
abstracter = Abstracter()

iterationList = []
correctList = []
num = 0

correct = 0
for (expression, answer) in validSet:
    expr = run_model(expression, answer, answer_maxlen, training = False, debug = False)
    if expr == expression + answer:
        correct += 1
        print("Correct! Given {} found {}".format(expression, expr))
    else: 
        print("Wrong! Given {} found {} instead of {}".format(expression, expr, expression+answer))
print(correct/len(validSet))
iterationList.append(num)
num += 1
correctList.append(correct/len(validSet))


for iteration in range(babble_iterations):
    for (expression, answer) in trainingSet:
        if random_order:
            (expression, answer) = r.choice(trainingSet)
        run_model(expression, answer, answer_maxlen, True)

correct = 0
for (expression, answer) in validSet:
    expr = run_model(expression, answer, answer_maxlen, training = False, debug = False)
    if expr == expression + answer:
        correct += 1
        print("Correct! Given {} found {}".format(expression, expr))
    else:
        print("Wrong! Given {} found {} instead of {}".format(expression, expr, expression+answer))
print(correct/len(validSet))
iterationList.append(num)
num += 1
correctList.append(correct/len(validSet))



for iteration in range(imitation_iterations):
    for (expression, answer) in trainingSet:
        if r.random() < 10/len(trainingSet):
            print("#", flush = True, end = "")
        if random_order:
            (expression, answer) = r.choice(trainingSet)
        expr = run_model(expression, answer, answer_maxlen, training = True, imitation = True)
        if iteration >= abstract_after_iteration:
            d = abstracter.equalityFinder(expr, solver, debug = False)
            #print(d, flush = True)
    print(flush = True)
    #print(abstracter.structures)
    correct = 0
    for (expression, answer) in validSet:
        (expr, structs) = run_model(expression, answer, answer_maxlen, training = False, debug = True)
        if expr == expression + answer:
            correct += 1
            print("Correct! Given {} found {}".format(expression, expr))
        else:
            print("Wrong! Given {} found {} instead of {}".format(expression, expr, expression+answer))
            print(structs)
    print(correct/len(validSet))
    iterationList.append(num)
    num += 1
    correctList.append(correct/len(validSet))

plotter.improvedPlot(iterationList, correctList, title = info, xlabel = "Iteration", ylabel = "Accuracy", figname = short_info + "Model.png")
