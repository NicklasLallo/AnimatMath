from Solver2 import *
from Abstracter2 import *

import random as r
import math as m

fraction_as_validation = 0.1
babble_iterations = 2
imitation_iterations = 100
abstract_after_iteration = 5
random_order = False

explore_rate = 0.01
solver_depth = 4
abstracter_depth = 2
answer_maxlen = 4
learning_rate = 0.9
discount_rate = 0.9
action_list = ["1","2","3","4","5","6","7","8","9","0","RETURN"]


solver = Solver(action_list, learning_rate, discount_rate)
abstracter = Abstracter()


trainingSet = []
validSet = []

for x in range(10):
    trainingSet.append("{}={}".format(x,x))
    for y in range(10):
        trainingSet.append("{}*{}={}".format(x,y,x*y))
        for z in range(10):
            trainingSet.append("{}*{}*{}={}".format(x,y,z,x*y*z))

for n in range(m.ceil(len(trainingSet)*fraction_as_validation)):
    i = r.randrange(0, len(trainingSet))
    validSet.append(trainingSet[i])
    del trainingSet[i]


def abstractSequenceAndGoal(sequence, debug = False):
    (goalRule, goal, newSequence, structs, action, value) = abstracter.structureTreeSearch(sequence, abstracter_depth, solver = solver, returnImmediately = 0.9, debug = debug, visitedNodes = set())
    if debug:
        print((newSequence, goal, action, value))
    if newSequence == None:
        return (sequence, {})
    return (newSequence, {goal: (action, value) })

def run_model(sequence, maxlen = 4, training = False, imitation = False, debug = False):
    expr = sequence
    if not imitation:
        i = sequence.index("=")
        expr = sequence[0:i+1]
    
    (absExpr, absGoal) = abstractSequenceAndGoal(expr, debug = debug)

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
        action = solver.improvedProgram(expr, solver_depth, absExpr, exploreProb, action, reward, absGoal)
        if action == "RETURN":
            reward = -1
            if not training:
                action = None
                reward = None
            elif expr in  trainingSet or expr in validSet:
                reward = 1
            solver.improvedProgram(expr+"D", 0, absExpr+"D", 1, action, reward, {})
            return expr
        reward = 0
        expr += action
        (absExpr, absGoal) = abstractSequenceAndGoal(expr)
    return expr

for iteration in range(babble_iterations):
    for expression in trainingSet:
        if random_order:
            expression = r.choice(trainingSet)
        run_model(expression, answer_maxlen, True)

for iteration in range(imitation_iterations):
    for expression in trainingSet:
        if r.random() < 10/len(trainingSet):
            print("#", flush = True, end = "")
        if random_order:
            expression = r.choice(trainingSet)
        expr = run_model(expression, answer_maxlen, False, True)
        if iteration >= abstract_after_iteration:
            d = abstracter.equalityFinder(expr, solver, debug = False)
            #print(d, flush = True)
    print(flush = True)
    print(abstracter.structures)
    correct = 0
    for expression in validSet:
        expr = run_model(expression, answer_maxlen, training = False, debug = True)
        if expr in validSet:
            correct += 1
        print("Given {} found {}".format(expression, expr))

    print(correct/len(validSet))

