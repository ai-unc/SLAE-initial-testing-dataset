import nltk
from nltk import word_tokenize
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from nltk.corpus import PlaintextCorpusReader

def tfidf(folder_path):
    file_pattern = r'.*\.txt'
    corpus = PlaintextCorpusReader(folder_path, file_pattern)

    documents = [corpus.raw(file_id) for file_id in corpus.fileids()]
    tokens = [word_tokenize(doc.lower()) for doc in documents]
    dictionary = Dictionary(tokens)
    corpus_bow = [dictionary.doc2bow(doc) for doc in tokens]

    return TfidfModel(corpus_bow)

# weights = tfidf[corpus_bow[0]]

# weights = [(dictionary[pair[0]], pair[1]) for pair in weights]

# pprint(sorted(weights, key=lambda weights: weights[1], reverse=True)[1:50])