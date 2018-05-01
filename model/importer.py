import math as m
import random as r

def importData(trainingFileName, validFileName = None, fraction_as_validation = 0.1):
    trainingFile = open(trainingFileName, "r")
    lines = trainingFile.readlines()
    lines = list(map(lambda x: x[:-1], lines))
    trainingFile.close()
    header = lines.pop(0)

    splitChar = " "
    splitCharPos = header.find("splitChar:")
    if splitCharPos != -1 and splitCharPos+10 < len(header):
        splitChar = header[splitCharPos+10]
    
    actionList = ["RETURN"]
    actionListPos = header.find("actionList:")
    if actionListPos != -1:
        pos = 11+actionListPos
        while pos < len(header) and header[pos] != splitChar:
            actionList.append(header[pos])
            pos += 1

    chars = []
    charsPos = header.find("chars:")
    if charsPos != -1:
        pos = charsPos+6
        while pos < len(header) and header[pos] != splitChar:
            chars.append(header[pos])
            pos += 1

    id_to_word = {}
    wordsPos = header.find("words:\"")
    if wordsPos != -1:
        pos = 7+wordsPos
        while pos < len(header) and header[pos] != "\"":
            if header[pos] == splitChar:
                pos += 1
                continue
            nextWord = ""
            while pos < len(header) and header[pos] != splitChar and header[pos] != "\"":
                nextWord += header[pos]
                pos +=1
            char = chars[len(id_to_word)]
            id_to_word[char] = nextWord

    trainingSet = []
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

    return (trainingSet, validSet, chars, actionList, id_to_word)
