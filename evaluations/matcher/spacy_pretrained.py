import spacy
nlp = spacy.load('en_core_web_lg')

def similar_words(text, word):
    doc = nlp(text)
    seed_word = nlp(word)

    similar_words=[word.text for word in doc if word.similarity(seed_word) > 0.7]
    return similar_words