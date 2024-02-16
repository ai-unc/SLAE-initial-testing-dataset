import gensim
import nltk
from gensim.models import word2vec, Phrases, Word2Vec
from gensim.models.phrases import Phraser
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams


def embedding(text, search_words):

    stop_words = set(stopwords.words('english'))
    stop_words.update(['the','of','and','in','to','a','an','was','as','by','for','is','on','at','onn','that','with'])
    token = nltk.word_tokenize(text)
    token_cleaned = [word for word in token if word.lower() not in stop_words and word not in punctuation]

    text_cleaned = ' '.join(token_cleaned)

    sentences = nltk.sent_tokenize(text_cleaned)
    bigram =Phraser(Phrases(sentences, min_count=1))
    trigram = Phraser(Phrases(bigram[sentences],min_count=1))

    trigram_sentences_project = []
    for sent in sentences:
        bigrams_ = bigram[sent.split(" ")]
        trigrams_ = trigram[bigram[sent.split(" ")]]
        trigram_sentences_project.append(trigrams_)

    # Defining parameters
    num_features = 200 # Word Vector Dimensionality (How many number in one vector?)
    min_word_count = 1 # Minimum word count
    num_workers = 20 # Number of threads to run in parallel
    context = 5 #Context window size
    downsampling = 1e-3 # Downsample setting for frequent word

    model = word2vec.Word2Vec(trigram_sentences_project,
                              workers=num_workers,
                              vector_size=num_features,
                              min_count=min_word_count,
                              window=context,
                              sample=downsampling)
    if isinstance(search_words, list):
        for word in search_words:
            print(f"Most similar words to '{word}':")
            print(model.wv.most_similar(word, topn=10))
    elif isinstance(search_words, str):
        print(f"Most similar words to '{search_words}':")
        print(model.wv.most_similar(search_words, topn=10))

        


def cosine_similarity(text, word1, word2):

    stop_words = set(stopwords.words('english'))
    stop_words.update(['the','of','and','in','to','a','an','was','as','by','for','is','on','at','onn','that','with'])
    token = nltk.word_tokenize(text)
    token_cleaned = [word for word in token if word.lower() not in stop_words and word not in punctuation]

    text_cleaned = ' '.join(token_cleaned)

    sentences = nltk.sent_tokenize(text_cleaned)
    bigram =Phraser(Phrases(sentences, min_count=1))
    trigram = Phraser(Phrases(bigram[sentences],min_count=1))

    trigram_sentences_project = []
    for sent in sentences:
        bigrams_ = bigram[sent.split(" ")]
        trigrams_ = trigram[bigram[sent.split(" ")]]
        trigram_sentences_project.append(trigrams_)

    # Defining parameters
    num_features = 200 # Word Vector Dimensionality (How many number in one vector?)
    min_word_count = 1 # Minimum word count
    num_workers = 20 # Number of threads to run in parallel
    context = 5 #Context window size
    downsampling = 1e-3 # Downsample setting for frequent word

    model = word2vec.Word2Vec(trigram_sentences_project,
                              workers=num_workers,
                              vector_size=num_features,
                              min_count=min_word_count,
                              window=context,
                              sample=downsampling)
    return f"The score between {word1} and {word2} is {model.wv.relative_cosine_similarity(word1, word2)}"

def embedding_stemmed(text, search_words):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['the','of','and','in','to','a','an','was','as','by','for','is','on','at','onn','that','with'])
    porter = PorterStemmer()

    
    token = nltk.word_tokenize(text)

    token_cleaned_stemmed = [porter.stem(word) for word in token if word.lower() not in stop_words and word not in punctuation]

    text_stemmed = ' '.join(token_cleaned_stemmed)

    sentences = nltk.sent_tokenize(text_stemmed)
    bigram =Phraser(Phrases(sentences, min_count=1))
    trigram = Phraser(Phrases(bigram[sentences],min_count=1))

    trigram_sentences_project = []
    for sent in sentences:
        bigrams_ = bigram[sent.split(" ")]
        trigrams_ = trigram[bigram[sent.split(" ")]]
        trigram_sentences_project.append(trigrams_)

    # Defining parameters
    num_features = 200 # Word Vector Dimensionality (How many number in one vector?)
    min_word_count = 1 # Minimum word count
    num_workers = 20 # Number of threads to run in parallel
    context = 5 #Context window size
    downsampling = 1e-3 # Downsample setting for frequent word

    model = word2vec.Word2Vec(trigram_sentences_project,
                              workers=num_workers,
                              vector_size=num_features,
                              min_count=min_word_count,
                              window=context,
                              sample=downsampling)
    if isinstance(search_words, list):
        for word in search_words:
            print(f"Most similar words to '{word}', stemmed form:{porter.stem(word)}:")
            print(model.wv.most_similar(porter.stem(word), topn=10))
    elif isinstance(search_words, str):
        print(f"Most similar words to '{search_words}', stemmed form:{porter.stem(search_words)}:")
        print(model.wv.most_similar(porter.stem(search_words), topn=10))