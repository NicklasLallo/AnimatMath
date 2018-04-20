

#Arithemetic - equality, single, and double multiplication tabled with single digit operands

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

