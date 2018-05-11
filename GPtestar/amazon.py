import json
import re

#Custom splitchar now that blankspace isn't as useful
splitchar = "$"

# To get the raw input datafiles, see this website: http://jmcauley.ucsd.edu/data/amazon/ 
data = json.load(open('data.json'))


#Output filename
f = open("naturallanguage.dat", "w")

#Manualy writing out the characters. Not optimal
f.write("splitChar:" + splitchar + "actionList:QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.1234567890 chars:QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.1234567890\n")


i = 1
for entry in data:
    row = entry["reviewText"] #Ignore all other fields from the raw input data
    row = re.sub(r'[^a-zA-Z0-9., ]', '', row) #Remove all special characters with regular expressions
    row = str(row) #Probably doesn't do anything, can be removed?
    row = re.split(" ", row) #Make it from a single long string into an list of words
    #print("{}\n".format(len(row)))
    row2 = row[-8:] #Make the 8 last words into the output
    row = row[:-8] #Make all except the 8 last words into the input
    for word in row:
        f.write(word + " ") 
    f.write(splitchar)
    for word in row2:
        f.write(word + " ")
    f.write("\n")
    i += 1

    if i == 100000: #Limit the number of lines to be processed in order to save time and space currently
        break

f.close()
