# Script to extract author, book, reviewer, and date from file name
# Takes in txt files to extract the file names
# Outputs CSV with author, title, reviewer, date, and original file name columns
# by Jack Hester

# Arguments:
# --inputDir [path to folder with txt files to extract titles from]
# --outputDir [where to store the output csv folder]
# --separator [separator used in file name for each segment, ex: _]

import os
import re
import csv
import argparse
import glob

# ask user for input directory, output directory, separator
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--routine", help="Pick the routine you want to run (build or divide_names")
parser.add_argument("-i", "--inputDir", help="Directs to the input to your corpus directory (for build)")
parser.add_argument("-if", "--inputFile", help="Directs to the input csv file (for divide_names)")
parser.add_argument("-o", "--outputDir", help="Directs to the output directory for your output table")
parser.add_argument("-s", "--separator", help="The separator you use to distinguish between pieces of file title (name, date, author, etc.)")
args = parser.parse_args()

routineChoice = args.routine
outputFolder = args.outputDir

def buildTable():
    inputFolder = args.inputDir
    separator = args.separator

    print("Generating a table from files in "+inputFolder+".")
    print("The CSV will be outputted to "+outputFolder+".")


    os.chdir(inputFolder)

    # create n-D list with split file names for each file
    # and create list of all file names to correlate
    splitFileNames = []
    fileNames = []
    for file in glob.glob("*.txt"):
        fileStr = file.replace(',','')
        fileStr = fileStr.replace('’','\'')
        fileStr = fileStr.replace('‘','\'')
        fileNames.append(fileStr)
        currList = []
        j = 0 # index of each piece of file's name in sub-list
        splitName = file.split(separator)
        while j<len(splitName):
            currName = splitName[j]
            currName=currName.encode().decode()
            if j == 0 or j==2:
                currName = re.sub('\d', '', currName)
            if j < 3:
                currName = currName.replace('-',' ')
            else:
                currName = currName.replace('.txt','')
            currName = currName.replace(',','')
            currName = currName.replace('’','\'')
            currName = currName.replace('‘','\'')
            currName = currName.replace('|','')
            currList.append(currName)
            j = j+1
        splitFileNames.append(currList)

    # Build csv file based on file name/split file name lists
    os.chdir(outputFolder)
    with open('book-table.csv', 'w+') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Author', 'Title', 'Reviewer', 'Date', 'FileName'])
        for index in range(0, len(splitFileNames)):
            filewriter.writerow([splitFileNames[index][0],splitFileNames[index][1],splitFileNames[index][2],splitFileNames[index][3],fileNames[index]])
    csvfile.close()

    print('Output CSV was successfully written to: '+outputFolder+'/book-table')

def div(part):
    authorCol = []
    authorCol.append("author_"+part)
    reviewerCol = []
    reviewerCol.append("reviewer_"+part)
    input = args.inputFile
    f = open(input, encoding='mac_roman')
    data = [item for item in csv.reader(f)]
    for i in range(1, len(data)):
        if part=='first':
            authorFirst = data[i][0].split(" ")[0]
            reviewerFirst = data[i][2].split(" ")[0]
            authorCol.append(authorFirst)
            reviewerCol.append(reviewerFirst)
        elif part=='last':
            authorLast = data[i][0].split(" ",1)[1]
            reviewerLast = data[i][2].split(" ",1)[1]
            authorCol.append(authorLast)
            reviewerCol.append(reviewerLast)
        else:
            print("Please specify first/last name (first or last)")
    f.close()

    new_data = []
    for x, item in enumerate(data):
        try:
            item.append(authorCol[x])
            item.append(reviewerCol[x])
        except IndexError as e:
            item.append("NA")
        new_data.append(item)
    f = open(outputFolder+part+'-name-csv.csv', 'w+')
    csv.writer(f).writerows(new_data)
    f.close()


if routineChoice=='build':
    buildTable()
elif routineChoice=='divide_names':
    partToDivide = input("Which part of name? (first or last): ")
    div(partToDivide)
else:
    print("ERROR: Please select a routine.")
    print('build for building a table')
    print('divid_names to crete a second table that has author and review first name colums (for genderapi use)')

