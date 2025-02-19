from Solver import *
from Abstracter import *

import random as r
import math as m
import plotter
import importer

def run_learner_test(fraction_as_validation = 0.1, trainingFileName = "arithmetic1.dat", answer_maxlen = 3, abstracter_depth = 2):

    #trainingFileName = "grammar1.dat"   #The file containing the training data
    validFileName = None                #The file containing the validation set, if None the validation data will be drawn as a fraction of the training data
    #fraction_as_validation = 0.9       #The fraction of the training data that will be taken for validation, only used if validFileName is None
    
    babble_iterations = 1           #How many iterations the system will be trained on what its actions does
    imitation_iterations = 4        #How many iterations the system will be trained on what output is good
    abstract_after_iteration = 1    #After how many imitation iterations will the system begin to make equality abstractions
    random_order = False            #Whether or not the data will be randomly drawn from the dataset
    
    explore_rate = 0.01     #When training and not imitating, how often will the system make a random move
    solver_depth = answer_maxlen        #How deep will the tree-search of the solver go
    #abstracter_depth = 1    #How deep will the tree-search of the abstracter go
    #answer_maxlen = 1       #How many actions can the system make before being forced to return
    learning_rate = 0.9     #Learning rate of the system
    discount_rate = 0.9     #Discount rate of the system
    action_list = ["1","2","3","4","5","6","7","8","9","0","RETURN"]    #List of actions the system can take, can be changed by importData()
    
    info = "DataSet: {}\nFraction used for validation: {}\nBabble iterations: {}\nSolver depth: {}\nAbstracter depth: {}".format(trainingFileName[:-4], fraction_as_validation, babble_iterations, solver_depth, abstracter_depth)
    short_info = "{}_{}_{}_{}".format(trainingFileName[:-4], fraction_as_validation, solver_depth, abstracter_depth)
    
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
            if debug:
                return (expr, structs)
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
                if not training:
                    action = None
                    reward = None
                solver.improvedProgram(expr+"D", 0, absExpr+"D", 1, action, reward, {}, training = training)
                if debug:
                    return (expr, structs)
                return expr
            reward = 0
            expr += action
            (absExpr, absGoal, structs) = abstractSequenceAndGoal(expr)
        solver.improvedProgram(expr, 0, absExpr, 1, action, 0, {}, training = training)
        reward = -1
        if expr == sequence + expected_output:
            reward = 1
        solver.improvedProgram(expr+"D", 0, absExpr+"D", 1, "RETURN", reward, {}, training = training)
    
        if debug:
            return (expr, structs)
        return expr
    
    def run_validation(num, saveFailures = False):
        correct = 0
        f = open("Wrong_" + short_info + ".txt","a+")
        for (expression, answer) in validSet:
            expr = run_model(expression, answer, answer_maxlen, training = False, debug = False)
            
            if using_words:
                expr2 = decode_sentence(expr)
                expression2 = decode_sentence(expression)
                answer2 = decode_sentence(answer)
            else:
                expr2 = expr
                expression2 = expression
                answer2 = answer
            
            if expr == expression + answer:
                correct += 1
                print("Correct! Given \"{}\" found \"{}\"".format(expression2, expr2))
            else: 
                print("Wrong! Given \"{}\" found \"{}\" instead of \"{}\"".format(expression2, expr2, expression2+answer2))
                if saveFailures:
                    f.write(expression2 + answer2 + "\n")
        print(correct/len(validSet))
        iterationList.append(num)
        correctList.append(correct/len(validSet))
        f.close()
    
    def decode_sentence(expr):
        sentence = ""
        for char in expr:
            sentence += id_to_word[char] + " "
        return sentence[:-1]
    
    
    (trainingSet, validSet, chars, action_list, id_to_word) = importer.importData(trainingFileName, validFileName, fraction_as_validation)
    
    if len(id_to_word) > 0:
        using_words = True
    else:
        using_words = False
    
    solver = Solver(action_list, learning_rate, discount_rate)
    abstracter = Abstracter()
    
    iterationList = []
    correctList = []
    num = 0
    
    run_validation(num)
    num+=1
    
    for iteration in range(babble_iterations):
        for (expression, answer) in trainingSet:
            if random_order:
                (expression, answer) = r.choice(trainingSet)
            run_model(expression, answer, answer_maxlen, True)
    
    run_validation(num)
    num+=1
    
    for iteration in range(imitation_iterations):
        for (expression, answer) in trainingSet:
            if r.random() < 10/len(trainingSet):
                print("#", flush = True, end = "")
            if random_order:
                (expression, answer) = r.choice(trainingSet)
            expr = run_model(expression, answer, answer_maxlen, training = True, imitation = True)
            if iteration == abstract_after_iteration:
                d = abstracter.equalityFinder(expr, solver, debug = False)
                #print(d, flush = True)
        print(flush = True)
        #print(abstracter.structures)
        run_validation(num, saveFailures = iteration == imitation_iterations-1)
        num+=1
    
    plotter.improvedPlot(iterationList, correctList, title = short_info, xlabel = "Iteration", ylabel = "Accuracy", figname = short_info + "Model.png")
    return (iterationList, correctList, short_info)
