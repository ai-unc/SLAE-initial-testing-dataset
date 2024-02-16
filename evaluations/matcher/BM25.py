import pandas as pd
from rank_bm25 import *
from string import punctuation
import nltk
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import PorterStemmer
from nltk.corpus import PlaintextCorpusReader


stop_words = STOPWORDS.union(set(['the','of','and','in','to','a','an','was','as','by','for','is','on','at','onn','that','with']))
def remove_stopwords(lst):
    tokenized_cleaned = list()
    for str in lst:
        tokens = nltk.word_tokenize(str)
        tokens_cleaned = [word for word in tokens if not word.lower() in stop_words and not word in punctuation]
        str_cleaned = " ".join(tokens_cleaned)
        tokenized_cleaned.append(str_cleaned)

def get_scores(folder_path, query):
    file_pattern = r'.*\.txt'
    corpus = PlaintextCorpusReader(folder_path, file_pattern)

    documents = [corpus.raw(file_id) for file_id in corpus.fileids()]
    lst1 =  remove_stopwords(documents)
    tokenized_corpus = [doc.split(" ") for doc in lst1]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query=query.split(" ")
    return bm25.get_scores(tokenized_query)
