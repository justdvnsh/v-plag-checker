import requests
import json
import urllib
import re
from backend.utils.ngram import find_similarity_n_grams_in_text, find_ngrams

def plag_for_text(text):

    features = find_ngrams(text)

    data = []

    for feature in features:
        print(feature)
        
        text_url_encoded = urllib.parse.quote(feature)

        print(text_url_encoded)

        response = requests.get('https://www.googleapis.com/customsearch/v1/siterestrict?key=AIzaSyBPRakZQjv780pIeU1w_v5m0so7AZHT7c0&cx=017168851564985857371:ocrlfzfoqwy&q={}'.format(text_url_encoded))

        response = json.loads(response.text)

        if 'items' in response:
            for items in response['items']:
                score_title = find_similarity_n_grams_in_text(feature, items['title'])
                score_snippet = find_similarity_n_grams_in_text(feature, items['snippet'])
                avg_score = score_snippet + score_title / 2

                print('AVG_SCORE: ',avg_score)
                if avg_score > 0.0:
                    data.append({
                        'feature': feature,
                        'title': items['title'],
                        'similarity_with_title': score_title,
                        'snippet': items['snippet'],
                        'similarity_with_snippet': score_snippet,
                        'average_score': avg_score,
                        'url': items['link']
                    })
                print('####################################################\n')
        else:
            continue

    final_score = [feature['average_score'] for feature in data]

    return data, final_score        

# data, final_score = plag_for_text('The cat was playing in the garden')
# print(len(data))
# print(final_score)

# plagiarizm = sum(final_score) / len(final_score)
# print(plagiarizm)
# for feature in data:
#     print(feature)

def plag_for_file(file):

    with open(file, 'r') as fl:
        text = fl.read()

    features = find_ngrams(text)

    data = []

    for feature in features:
        print(feature)
        
        text_url_encoded = urllib.parse.quote(feature)

        print(text_url_encoded)

        response = requests.get('https://www.googleapis.com/customsearch/v1/siterestrict?key=AIzaSyBPRakZQjv780pIeU1w_v5m0so7AZHT7c0&cx=017168851564985857371:ocrlfzfoqwy&q={}'.format(text_url_encoded))

        response = json.loads(response.text)

        # print(response)
        if 'items' in response:
            for items in response['items']:
                score_title = find_similarity_n_grams_in_text(feature, items['title'])
                score_snippet = find_similarity_n_grams_in_text(feature, items['snippet'])
                avg_score = score_snippet + score_title / 2

                print('AVG_SCORE: ',avg_score)
                if avg_score > 0.0:
                    data.append({
                        'feature': feature,
                        'title': items['title'],
                        'similarity_with_title': score_title,
                        'snippet': items['snippet'],
                        'similarity_with_snippet': score_snippet,
                        'average_score': avg_score,
                        'url': items['link']
                    })
                print('####################################################\n')

        else:
            continue

    final_score = [feature['average_score'] for feature in data]

    return data, final_score        

# data, final_score = plag_for_file('shake_1.txt')    
# print(len(data))
# print(final_score)

# plagiarizm = sum(final_score) / len(final_score)
# print(plagiarizm)

# print(plag_for_file('shake_1.txt'))