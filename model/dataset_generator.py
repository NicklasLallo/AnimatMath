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
operands = ["*","+"]

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

