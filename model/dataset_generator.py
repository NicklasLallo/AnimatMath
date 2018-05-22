operands = ["*","+"]
def operator(op, x, y):
    if op == "*":
        return x*y 
    else: 
        return x+y

characters = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
#arithemetic1.dat - equality, single, and double multiplication tabled with single digit operands

dataSet = []

for x in range(300):
    dataSet.append("{}= {}".format(x,x))

for x in range(10):
    for y in range(10):
        dataSet.append("{}*{}= {}".format(x,y, x*y))
        for z in range(10):
            dataSet.append(("{}*{}*{}= {}".format(x,y,z, x*y*z)))

f = open("arithmetic1.dat", "w")
f.write("splitChar: actionList:1234567890 description:\"Equalities from 0 to 300 and alla single digit multiplications with one and two multiplicants\" chars:1234567890*= \n")
for data in dataSet:
    f.write(data+"\n")
f.close()


#arithmetic2.dat - arithmetic1 with + as addition

dataSet = []

for x in range(300):
    dataSet.append("{}= {}".format(x,x))

for x in range(10):
    for y in range(10):
        for op1 in operands:
            ans = operator(op1,x,y)
            dataSet.append("{}{}{}= {}".format(x,op1,y, ans))
            for z in range(10):
                for op2 in operands:
                    if op1 == "*":
                        ans = operator(op2, operator(op1, x, y), z)
                    else:
                        ans = operator(op1, operator(op2, y, z), x)
                    dataSet.append(("{}{}{}{}{}= {}".format(x,op1,y,op2,z, ans)))

f = open("arithmetic2.dat", "w")
f.write("splitChar: actionList:1234567890 chars:1234567890*+=\n")
for data in dataSet:
    f.write(data+"\n")
f.close()


#logic1.dat - expressions with logic AND and OR with up to three operators

dataSet = []

for x in range(2):
    dataSet.append("{}= {}".format(x, x))
    for y in range(2):
        for z in range(2):
            if not y:
                r1 = x and z
            else:
                r1 = x or z
            dataSet.append("{}{}{}= {}".format(x,operands[y],z,r1*1))
            for v in range(2):
                for w in range(2):
                    if not v:
                        r2 = r1 and w
                    else:
                        r2 = r1 or w
                    dataSet.append("{}{}{}{}{}= {}".format(x,operands[y],z,operands[v],w,r2*1))
                    for h in range(2):
                        for g in range(2):
                            if not h:
                                result = r2 and g
                            else:
                                result = r2 or g
                            dataSet.append("{}{}{}{}{}{}{}= {}".format(x,operands[y],z,operands[v],w,operands[h],g,result*1))

f = open("logic1.dat", "w")
f.write("splitChar: actionList:10 chars:10+*=\n")
for data in dataSet:
    f.write(data+"\n")
f.close()

#arithmetic3.dat - arithmetic2 with double digit characters

dataSet = []

for x in range(10000):
    dataSet.append("{}= {}".format(x,x))

for x in range(100):
    for y in range(100):
        for op1 in operands:
            ans = operator(op1,x,y)
            dataSet.append("{}{}{}= {}".format(x,op1,y, ans))
            for z in range(100):
                for op2 in operands:
                    if op1 == "*":
                        ans = operator(op2, operator(op1, x, y), z)
                    else:
                        ans = operator(op1, operator(op2, y, z), x)
                    dataSet.append(("{}{}{}{}{}= {}".format(x,op1,y,op2,z, ans)))

f = open("arithmetic3.dat", "w")
f.write("splitChar: actionList:1234567890 chars:1234567890*+=\n")
for data in dataSet:
    f.write(data+"\n")
f.close()


#grammar1.dat - simple english grammar
hesheit = ["he", "she", "it"]
rest = ["they", "we", "I", "you"]
pronouns = ["he", "she", "it", "they", "we", "I", "you"]
verbs = ["talk", "walk", "remember", "dream", "pay", "call", "play"]
verb_bends = ["ed"]
doing = ["he is", "she is", "it is", "they are", "we are", "I am", "you are", "he's", "she's", "it's", "they're", "we're", "I'm", "you're"]
doings = ["fun", "unpleasant", "delightful", "free", "old", "young", "active", "correct", "wrong"]

good_sentences = []
good_sentences += [x + " " + y + z for x in pronouns for y in verbs for z in verb_bends]
good_sentences += [x + " " + y + "s" for x in hesheit for y in verbs]
good_sentences += [x + " " + y  for x in rest for y in verbs]
good_sentences += [x + " " + y for x in doing for y in doings]
good_sentences += [x + " " + y + "ing" for x in doing for y in verbs]

bad_sentences = []
bad_sentences += [x + " " + y for x in pronouns for y in doings]
bad_sentences += [x + " " + y for x in doing for y in verbs]
bad_sentences += [x + " " + y + z for x in doing for y in verbs for z in verb_bends]
bad_sentences += [x + " " + y for x in doings for y in doing]

words = set(["(Yes)", "(No)"])
nr = 2
wordString = "(Yes) (No) "
word_to_id = {"(Yes)": "1", "(No)": "2"}
for sentence in good_sentences + bad_sentences:
    splits = sentence.split()
    for word in splits:
        if word not in words:
            words.add(word)
            wordString += word + " "
            word_to_id[word] = characters[nr]
            nr += 1

f = open("grammar1.dat", "w")
f.write("splitChar: actionList:12 chars:{} words:\"{}\"\n".format(characters[:len(words)], wordString))
for sentence in good_sentences:
    splits = sentence.split()
    for word in splits:
        f.write(word_to_id[word])
    f.write(" 1\n")
for sentence in bad_sentences:
    splits = sentence.split()
    for word in splits:
        f.write(word_to_id[word])
    f.write(" 2\n")
f.close()

f = open("grammar1.txt", "w")
for sentence in good_sentences + bad_sentences:
    f.write(sentence + "\\\\\n")
f.close()
