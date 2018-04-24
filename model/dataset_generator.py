operands = ["*","+"]
def operator(op, x, y):
    if op == "*":
        return x*y 
    else: 
        return x+y

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
f.write("splitChar: actionList:1234567890\n")
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
f.write("splitChar: actionList:1234567890\n")
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
f.write("splitChar: actionList:10\n")
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
f.write("splitChar: actionList:1234567890\n")
for data in dataSet:
    f.write(data+"\n")
f.close()

