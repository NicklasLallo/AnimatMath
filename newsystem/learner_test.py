from Solver2 import *
from Abstracter2 import *

import random as r
import math as m

fraction_as_validation = 0.01
babble_iterations = 10
imitation_iterations = 100
abstract_after_iteration = 5
random_order = True

explore_rate = 0.01
solver_depth = 4
abstracter_depth = 4
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


def abstractSequenceAndGoal(sequence):
    (goalRule, goal, newSequence, structs) = abstracter.structureTreeSearch(sequence, abstracter_depth)
    if goalRule == None:
        return (sequence, {})
    return (newSequence, {goal: (goalRule[2][0], goalRule[3][0]) })

def run_model(sequence, maxlen = 4, training = False, imitation = False):
    expr = sequence
    if not imitation:
        i = sequence.index("=")
        expr = sequence[0:i+1]
    
    (absExpr, absGoal) = abstractSequenceAndGoal(expr)

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
        if random_order:
            expression = r.choice(trainingSet)
        expr = run_model(expression, answer_maxlen, False, True)
        if iteration >= abstract_after_iteration:
            d = abstracter.testStructureFormationRule(expr, solver)
    correct = 0
    for expression in validSet:
        expr = run_model(expression, answer_maxlen)
        if expr in validSet:
            correct += 1
    print(correct/len(validSet))

