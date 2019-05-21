# command line tool for implementing gensim
# by Jack Hester
# code partly based on "https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/"
# last updated 5/21/2019
# TODO: make GUI and save topics to a single text file separate from html
# WARNING: you may need to comment out line 29 (matplotlib.use(...)) especially if on windows

# Arguments:
# --inputDir [path to folder with txt files to analyze]
# --outputFileName [file name including path, ending with .html]

# Example usage:
# python /Users/jhester/Desktop/gensim-command-line.py  --inputDir /Users/jhester/Desktop/nyer --outputFileName /Users/jhester/Desktop/nyer-topics.html

import re
import glob
import os
import numpy as np
import pandas as pd
from pprint import pprint
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
import pyLDAvis
import pyLDAvis.gensim
import matplotlib
matplotlib.use('TkAgg') # may be necessary for your system
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import argparse

# get CLAs of input dir and output file name
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputDir", help="Directs the input to your text directory")
parser.add_argument("-o", "--outputFileName", help="Directs the output to a file name and path of your choice, MUST end in .html")
args = parser.parse_args()

outputFileName = args.outputFileName
inputFolder = args.inputDir

# TODO: print the outputs of topics and words in terminal as a csv file or table that's nicely formatted

os.chdir(inputFolder)
#os.chdir("/Users/jhester/Box Sync/Fall 2018 LING 499R-NLP/Bunin Faulkner Chong/reviews/nytout")

# import data:

os.listdir
content = []
for fileName in glob.glob("*.txt"):
    with open(fileName, 'r') as file:
        content.append(file.read())
    file.close()

#TODO: read in the article title in stead of an arbitrary number (1 here)
raw_data = {"title": 1, "content": content}

df = pd.DataFrame(data=raw_data)

data = df.content.values.tolist()


stop_words = stopwords.words('english')
# TODO: (optional) add more stop words that are common but unncesseary for topic modeling
#stop_words.extend(['','']

#TODO: import data

# tokenize, clean up, deacc true is removing the punctuation
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence),deacc=True))

data_words = list(sent_to_words(data))


# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# See trigram example
print(trigram_mod[bigram_mod[data_words[0]]])


# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

print(data_lemmatized[:1])

# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# View
print(corpus[:1])


########################################

# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=20,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)

# Print the Keywords in the topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

########################################

# visualize and generate html
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.prepared_data_to_html(vis)
try:
    #os.chdir("/Users/jhester/Desktop")
    pyLDAvis.save_html(vis,outputFileName)
except:
    print('file generation failed!')

# open and display
pyLDAvis.display(vis)
pyLDAvis.show(vis)
