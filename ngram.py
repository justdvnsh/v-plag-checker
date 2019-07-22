import nltk
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re, math
from collections import Counter
from cosineSim import cosineSim
from nltk.tokenize import word_tokenize

def find_ngrams(text):
    n = 3
    text = ngrams(text.lower().split(), n)

    data = []
    for grams in text:
        # data.append(gram)
        str2 =' '.join(grams) 
        data.append(str2)
        final2 = ', '.join(data)

    # print(data)
    return data
# find_ngrams('The cat was playing in the garden')    

def find_similarity_n_grams(fl1, fl2):
    n = 3

    with open(fl1, 'r') as fl:
        text1 = fl.read()

    with open(fl2, 'r') as fl:
        text2 = fl.read()        

    text1 = ngrams(text1.lower().split(), n)
    text2 = ngrams(text2.lower().split(), n)

    smaller_file = min(len(text1), len(text2))

    if smaller_file < n:
        n = smaller_file

    list1 = []
    list2 = []


    for grams in text1:
        # print(grams)
        str1=''.join(grams)
        list1.append(str1)
        final1 = ', '.join(list1)

    for grams in text2:
        # print(grams)
        str2 =''.join(grams) 
        list2.append(str2)
        final2 = ', '.join(list2)


    # print(list1)
    # print(list2)
    # print(final1)
    # print(final2)


    # print('Cosine:', cosineSim(final1, final2))

    return cosineSim(final1, final2)

def find_similarity_n_grams_in_text(text1, text2):

    text1 = text1.lower().split()
    text2 = text2.lower().split()

    # print(text2)
    smaller_text = min(len(text1), len(text2))

    n = 3

    if smaller_text < n:
        n = smaller_text

    text1 = ngrams(text1, n)
    text2 = ngrams(text2, n)

    list1 = []
    list2 = []


    for grams in text1:
        # print(grams)
        str1=''.join(grams)
        list1.append(str1)
        final1 = ', '.join(list1)

    for grams in text2:
        # print(grams)
        str2 =''.join(grams) 
        list2.append(str2)
        final2 = ', '.join(list2)

    # print(list1)
    # print(list2)
    # print(cosineSim(final1, final2))
    # print(final2)
    return cosineSim(final1, final2)

find_similarity_n_grams_in_text('The cat was playing in the garden', 'Halloween 2016')    
