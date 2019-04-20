Coreference Resolution on Directory of Files

File: Coref.java

Working with Stanford CoreNLP 3.9.2
---

HOW TO RUN:

1) Compile

javac -cp .:/[path to Stanford CoreNLP]* Coref.java

Example:
javac -cp .:/Users/jhester/Downloads/stanford-corenlp/* Coref.java

2) Run

java -Xmx6g -cp .:/[path to Stanford CoreNLP]* -inputDir [input directory path] -outputDir [output directory path] -approach [neural, statistical, deterministic]

Example:
java -Xmx6g -cp .:/Users/jhester/Downloads/stanford-corenlp/* Coref -inputDir /Users/jhester/Desktop/CorefTest/in-test -outputDir /Users/jhester/Desktop/CorefTest/out-test -approach neural

You can also run with just one file (not whole directory) with -inputFile rather than -inputDir

Example:
java -Xmx6g -cp .:/Users/jhester/Downloads/stanford-corenlp/* Coref -inputFile file.txt -outputDir /Users/jhester/Desktop/CorefTest/out-test -approach neural

---

NOTICES FOR USE ON WINDOWS:

All paths should be enclosed in "", especially on Windows systems

NOTICE Change \ of Windows OS to / of Apple OS
 
1. input folder name: -inputDir "C:\Users\rfranzo\Desktop\Sample texts"
All txt files in the folder will be processed for coreference resolution

2. output folder name: -outputDir "C:\Users\rfranzo\Desktop\NLP_output"

Example:

Change \ of Windows OS to / of Apple OS

Run the CD command to change to the directory where Coref is stored
cd "C:\Program Files (x86)\PC-ACE\NLP\Miscellaneous"

java -mx6g -cp ".:C:\Program Files (x86)\PC-ACE\NLP\StanfordCoreNLP" Coref -inputDir "C:\Users\rfranzo\Desktop\Sample texts" -outputDir "C:\Users\rfranzo\Desktop\NLP_output" -approach neural