import nltk
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re, math
from collections import Counter
from cosineSim import cosineSim
from nltk.tokenize import word_tokenize


def find_similarity_n_grams(fl1, fl2):

    n = 3

    with open(fl1, 'r') as fl:
        text1 = fl.read()

    with open(fl2, 'r') as fl:
        text2 = fl.read()        

    text1 = ngrams(text1.lower().split(), n)
    text2 = ngrams(text2.lower().split(), n)

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


    print('Cosine:', cosineSim(final1, final2))

    return cosineSim(final1, final2)

# # import os

# # data = {}
# # for _,_,files in os.walk('uploads'):
# #     for file in files:
# #         with open(file, 'r') as fl:
# #             data[file] = fl.read()

# # for keys in data.keys():
# #     grams = ngrams(data[keys].lower().split(), n)
# #     for gram in grams:
# #         print(gram)

# find_similarity_n_grams('shake_1.txt', 'shake_2.txt')

# data = [1,2,3,4,5,6,7,8,9]

# for i in range(len(data)):
#     # print(i)
#     if i == len(data) - 1:
#         break;
#     else:        
#         print(data[0], data[i+1])