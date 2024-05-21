import nltk
import numpy as np
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)

    for idx, w, in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag

# Tokeniziong a sentence
# a = "How long does shipping take?"
# print(a)
# print(tokenize(a))

# Getting stem of words
# words = ["Intentional", "Smithery", "Organization", "nonsensensical"]
# stemmed_words = [stem(w) for w in words]
# print(stemmed_words)

# Testing our bag_of_words function
# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thanks", "cool"]
# bag = bag_of_words(sentence, words)
# print(bag)