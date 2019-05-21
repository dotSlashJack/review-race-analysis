README for "gensim-cla.py"

This python file generates topic models and visualizations via gensim for a folder of .txt files (corpus)

It depends on:
re (Regular expression operations), glob, bumpy, pandas, pprint, gensim, spacy, pyLDAvis, matplotlib, nltk, and argparse

THESE MUST BE INSTALLED! This can be done largely through pip and/or Conda.

---


There are two command line arguments required:

--inputDir [path to folder with txt files to analyze]
--outputFileName [file name including path, ending with .html]


---

Example usage (Mac OS):

python /Users/jhester/Desktop/gensim-command-line.py  --inputDir /Users/jhester/Desktop/nyer --outputFileName /Users/jhester/Desktop/nyer-topics.html

---
Additional notes:

WARNING: you may need to comment out line 29 (matplotlib.use(...)) especially if on windows