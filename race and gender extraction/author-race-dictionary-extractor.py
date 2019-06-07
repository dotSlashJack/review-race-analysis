# Author Race Extractor
# By Jack Hester
# Matches cells within a csv and appends a new column with the race to the end of each row(s)
# This routine uses a folder with text files of authors based on their race/ethnicity
# This is a dictionary-based approach and will not necessarily find all authors
# The dictionary was last updated December 2018

import os
import glob
import argparse
import csv

# ask user for dictionary, csv of names, index of column 
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputFile", help="Directs to the input csv file (for divide_names)")
parser.add_argument("-c", "--column", type=int, help="Index of column with names, starting at 1 (not 0)")
parser.add_argument("-o", "--outputDir", help="Directs to the output directory for your output table")
parser.add_argument("-d", "--dictionary", help="Directs to the location of the txt files dictionary of race lists")
args = parser.parse_args()

inputFile = args.inputFile
outputFolder = args.outputDir
colToParse = args.column - 1
dictionary = args.dictionary

# match names in files if they exist
os.chdir(dictionary)
def match(currName):
    discoveredRace = "NA"
    i = 0
    for file in glob.glob("*.txt"):
        #print('looking through '+file)
        currRace = file.split('.txt')[0] # each file is named by the race of authors it contains
        with open(file) as f:
            line = f.readline()  
            while line:
                line = f.readline()
                #print(line)
                if currName in line:
                    discoveredRace = currRace
                    #print('Found one for '+currName)
                    return discoveredRace
                    break
        i=i+1
        f.close()
        if i == 70: # we've gone through every fil in the dictionary and it wasn't found
            discoveredRace = "NA"
            print('race not found for '+currName)
            break


raceCol = []
raceCol.append("Race")
f = open(inputFile, encoding='mac_roman')
data = [item for item in csv.reader(f)]

for i in range(1, len(data)):
    authorName = data[i][colToParse]
    raceCol.append(match(authorName))
f.close()

new_data = []
for x, item in enumerate(data):
    try:
        item.append(raceCol[x])
    except IndexError as e:
        item.append("NA")
    new_data.append(item)
f = open(outputFolder+'race-table.csv', 'w+')
csv.writer(f).writerows(new_data)
f.close()

#get the cell
#match within text file
#add to the end of the row
#match('hello')
