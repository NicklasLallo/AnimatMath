import json
import re
from pprint import pprint

splitchar = "$"
data = json.load(open('data.json'))


f = open("naturallanguage.dat", "w")

f.write("splitChar:" + splitchar + "actionList:qwertyuiopasdfghjklzxcvbnm,.1234567890\n chars:qwertyuiopasdfghjklzxcvbnm,.1234567890\n")
#for data in dataSet:
#    f.write(data+"\n")
#f.close()


i = 1
for entry in data:
    row = entry["reviewText"]
    row = re.sub(r'[^a-zA-Z0-9., ]', '', row)
    row = str(row)
    row = re.split(" ", row)
    #print("{}\n".format(len(row)))
    row2 = row[-8:]
    row = row[:-8]
    for word in row:
        f.write(word + " ")
    f.write(splitchar)
    for word in row2:
        f.write(word + " ")
    f.write("\n")
    i += 1

    if i == 100000:
        break
    #print("{}\n".format(len(row)))

f.close()
#print(len(data))
