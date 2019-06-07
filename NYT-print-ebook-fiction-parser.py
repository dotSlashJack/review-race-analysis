# NYT Book Review Web Parser, easily adaptable to other websites
# by Jack Hester
# Note: depends on beautifulsoup4, and urllib2!
# v 0.0.2, now able to use python 3.x
import argparse
import os
import re
import glob
import datetime as dt
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import time
from bs4 import BeautifulSoup as bs
import os.path
import sys
import warnings
import datetime
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
warnings.filterwarnings("ignore", category=UserWarning)
#reload(sys)
#sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--startDate", help="Week (must correspond to NYT week) to start at in format YYYY-mm-dd")
parser.add_argument("-n", "--weeksBack", type=int, help="Number of weeks back to attempt to search")
parser.add_argument("-o", "--outputDir", help="Directs the output to a path (folder) of your choice")
parser.add_argument("-c", "--checkTitles", help="(y/n) Attempt to automatically fix no-book-author titles")
args = parser.parse_args()

#nWeeks = 300
nWeeks = args.weeksBack # number of weeks back to go
startDate = datetime.datetime.strptime(args.startDate, '%Y-%m-%d')
outputFolder = args.outputDir
checkTitles = args.checkTitles
print("\n")
print("Algorithm will start from the date "+datetime.datetime.strftime(startDate, "%Y-%m-%d")+" and go backwards up to "+str(nWeeks)+" weeks.")

# configuring a set of dates to place in URLs to download from

#nWeeks = sys.argv[0]
#print('Going back '+ str(nWeeks) + ' weeks.')
#today = dt.date(2019, 6, 9)
today = startDate #set starting date (must correspond with NYT week)
dayMinus = 7
base_yr, base_mo, base_day = str(today.year), str(today.month), str(today.day)
if len(base_mo)==1:
    base_mo = '0'+base_mo
if len(base_day)==1:
    base_day = '0'+base_day
todayStr = base_yr+'/'+base_mo+'/'+base_day
reviewDates = [todayStr]


# Generating a list of times to place in URLs to check
for i in range(1, nWeeks+1):
    nDate = today - dt.timedelta(days=dayMinus)
    yr, mo, day = str(nDate.year), str(nDate.month), str(nDate.day)
    if len(mo)==1:
        mo = '0'+mo
    if len(day)==1:
        day = '0'+day
    dateStr = yr+'/'+mo+'/'+day
    reviewDates.append(dateStr)
    dayMinus += 7



# Generating a list of URLs to check for download links
baseURL = 'https://www.nytimes.com/books/best-sellers/'
urls = []
for i in range(0, nWeeks):
    urls.append(baseURL+reviewDates[i]+'/combined-print-and-e-book-fiction/')
print('Finished setting weeks (back) to check.')

dlList = [] # list of actual urls to download
currLink = '' # current link in page to download
currURL = '' # (selected) url of each week of book reviews
for i in range(0, nWeeks):
    currURL = urls[i]
    #if i>0 and i%30==0:
        #print('Paused to prevent server overload')
        #time.sleep(2) # prevent server request overload
        #print('Resumed')
    try:
        sauce = urllib2.urlopen(currURL).read()
        soup = bs(sauce)
        for a in soup.find_all('a', href=True, class_='review-link'):
            currLink = a['href']
            if currLink not in dlList:
                dlList.append(currLink)
    except:
        print('url may not exist past this point')
        break

print('Finished collecting article urls.')
print(dlList)
print()
#print('downloading'+str(len(dlList))+'articles')

# get the title
def title(currSoup):
    try:
        dateString = currSoup.time['datetime'] # got time from the article's html
        dateString = dateString.split('T')[0]
    except(TypeError, KeyError) as e:
        dateString='0001-01-01'
        pass
    #bookTitle = currSoup.find('strong', class_='css-8qgvsz euv7paa0').string
    #bookTitle = bookTitle.replace(' ','-') # replace spaces with dashes for easy ngrams use
    articleTitle = currSoup.find('title').string
    articleTitle = articleTitle.replace('- The New York Times','')
    articleTitle = articleTitle.replace(' ','-')
    articleTitle = articleTitle.replace('/','')
    articleTitle = articleTitle.replace('’','\'')
    articleTitle = articleTitle.replace('‘','\'')
    #author = currSoup.find('p', class_='css-1baulvz').contents[3] # get the authors
    try:
        author = currSoup.find('span', class_='css-1baulvz').string
    except(TypeError, KeyError, AttributeError) as e:
        author = 'article-author-error'
        pass
    try:
        bookAuthor = currSoup.find('span', class_='css-8i9d0s e13ogyst0').string
    except:
        try:
            bookAuthor = currSoup.find('span', class_='caption-text').string
        except:
            bookAuthor = 'no-book-author'
            pass

    #titleStr = author+articleTitle+','+dateString+'.txt' # ngram friendly file name
    if bookAuthor is None:
        bookAuthor = 'NO-BOOK-AUTHOR'
    if articleTitle is None:
        articleTitle = 'NO-ARTICLE-TITLE'
    if author is None:
        author = 'NO-ARTICLE-AUTHOR'
    if dateString is None:
        author = 'NO-DATE'

    titleStr = bookAuthor+'_'+articleTitle+'_'+author+'_'+dateString # ngram friendly file name
    titleStr = titleStr.replace('/','')
    return titleStr

# download the text, put in file
def download(currSoup, file):
    try:
        # This approach is a bit crude, it might be necessary to run mutiple, nested
        # try...catch loops and/or check if file is empty after each of these for loops
        for p in currSoup.find_all('p', class_='css-18icg9x evys1bk0'):
            #print(p)
            text = p.text
            file.write(str(text)+'\n')
        for p in currSoup.find_all('p', class_='story-body-text story-content'):
            text = p.text
            file.write(str(text)+'\n')
        for p in currSoup.find_all('p', class_='story-body story-body-1'):#[1:]:
            text = p.text
            file.write(str(text)+'\n')
    except(TypeError, KeyError) as e:
        print('ERROR: No text found in: ')
        print(currSoup)

# main loop, writes files for all of the reviews
length = int(len(dlList)) # number of the sublinks (articles) to download
print('Downloading '+str(length)+' articles and generating files, this may take a while!\n')
for i in range(0, length):
    sauceDL = urllib2.urlopen(dlList[i]).read()
    if i>0 and i%30==0:
        print('Paused to prevent server overload')
        time.sleep(15) # prevent server request overload
        print('Resumed')
    print(dlList[i])
    #print('index: '+str(i))
    soupDL = bs(sauceDL)
    #print(dlList[i])
    titleStr = title(soupDL)
    #save_path = '/Users/jhester/Box Sync/Fall 2018 LING 499R-NLP/NYT-fiction-Extraction/'
    save_path = outputFolder
    titleComplete = os.path.join(save_path, titleStr+'.txt')
    f = open(titleComplete,'w+')
    download(soupDL, f)
    f.close()

    complete = (i*100.0)/length
    sys.stdout.flush()
    sys.stdout.write(str(complete) + '% complete ')

print(str(length) + ' files outputted.')
print('\nComplete, check output folder!')

if(checkTitles == "y"):
    print('Editing titles to include book author where possible...')
    os.chdir(outputFolder)
    for fileName in glob.glob("*.txt"):
        authorStr = 'AUTHOR-EXTRACTION-FAILED'
        if('no-book-author' in fileName):
            with open(fileName, 'r') as file:
                firstLine = file.readline()
                if('By ' in firstLine):
                    authorStr = firstLine.split('By ')[1]
                    authorStr = authorStr.split('Read by')[0]
                    #break ahead of numbers
                    match = re.match(r"([a-z]+)([0-9]+)", authorStr, re.I)
                    if match:
                        items = match.groups()
                        authorStr = items[0]
                    authorStr = authorStr.split('?')[0]
                    authorStr = authorStr.split('.')[0]
                    authorStr = authorStr.split('!')[0]
                    authorStr = authorStr.replace('pp','')
                    authorStr.strip()
                    if authorStr=='':
                        authorStr = 'AUTHOR-EXTRACTION-FAILED'
                    if authorStr is None:
                        authorStr = 'AUTHOR-EXTRACTION-FAILED'
            file.close()
            newName = fileName.split('no-book-author_')[1]
            newName = authorStr+'_'+newName
            os.rename(fileName, newName)

#delete 1st line if it contains book information
os.chdir(outputFolder)
for file in glob.glob("*.txt"):
    with open(file, 'r') as f:
        firstLine = f.readline()
        if(' By ' in firstLine or '. $' in firstLine):
            lines = f.readlines()
            f.close()
            with open(file, 'w') as f:
                f.writelines(lines[1:])
    f.close()
