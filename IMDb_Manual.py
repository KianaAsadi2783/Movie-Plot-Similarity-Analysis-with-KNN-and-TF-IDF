import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import json
from nltk.corpus import stopwords
from math import log, sqrt
from collections import Counter
import numpy as np

def clean_text(text):
    text = re.sub(r"'s", '', text)
    text = re.sub(r"\.", '', text)
    text = re.sub(r"[^\w\s]", ' ', text)
    word_list = text.strip().split()
    cleaned_words = list(filter(lambda word: word not in set(stopwords.words('english')), word_list))
    text = ' '.join(cleaned_words)
    return text

def find_summaries(code):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    movie_page = requests.get(f'https://www.imdb.com/title/{code}/plotsummary/?ref_=tt_stry_pl', headers=header)
    movie_soup = BeautifulSoup(movie_page.text, 'html.parser')
    movie_name = movie_soup.find('h2', class_="sc-a885edd8-9 dcErWY").text
    summary_menu = movie_soup.find('section', class_="ipc-page-section ipc-page-section--base")
    summaries = summary_menu.find_all('li', class_="ipc-metadata-list__item")
    movie_summaries=''
    for summary in summaries:
        summary = summary.find('div', class_="ipc-html-content-inner-div").text.lower()
        summary = re.sub(r'—(.*)','' ,summary)
        movie_summaries += (" " + summary)
    return [movie_name, clean_text(movie_summaries)]

def calculate_idf(word):
    count = 0
    for i in range(len(main_list)):
        if word in main_list[i][1].split():
            count += 1
    return log(250/count, 10)+1

def calculate_tf(text):
    words = text.split()
    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    return {word: (count/total_words) for word, count in word_counts.items()}

def calculate_tfidf(title, word):
    if word not in idf_dict.keys():
        idf_dict[word] = calculate_idf(word)
    return round((tf_dict[title][word]) * (idf_dict[word]), 4)

def create_vector(movie):
        movie_vector = []
        for word in idf_dict.keys():
            if word in tfidf_dict[movie].keys():
                movie_vector.append(tfidf_dict[movie][word])
            else:
                movie_vector.append(0)
        return (movie,movie_vector)

def calculate_cosine_similarity(vector1,vector2):
        dot_product = np.dot(vector1, vector2)
        magnitude_input= sqrt(np.dot(vector1, vector1))
        magnitude_movie = sqrt(np.dot(vector2, vector2))
        similarity = dot_product / (magnitude_input * magnitude_movie)
        return similarity

def find_similar_movies():
    for movie in main_list:
        title, summary = movie
        tf_dict[title] = calculate_tf(summary)
        tfidf_dict[title] = {}
        for word in set(summary.split()):
            tfidf_dict[title][word] = calculate_tfidf(title, word)

    movie_vectors = []
    for movie in tfidf_dict:
        movie_vectors.append(create_vector(movie))
    input_vector = movie_vectors[-1][1]
    movie_array = np.array([movie_vector[1] for movie_vector in movie_vectors[:250]])

    similarity_scores = []
    for movie_vector in movie_array:
        similarity_scores.append(calculate_cosine_similarity(input_vector,movie_vector))

    similarity_list = []
    for i, score in enumerate(similarity_scores):
        similarity_list.append((movie_vectors[i][0], round(score, 4)))

    final_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)
    for i in range(5):
        print(final_list[i][0])

main_list = []
idf_dict ,tf_dict ,tfidf_dict = {},{},{} 

with open("Clean_Summaries.json", "r") as Clean_Summaries:
    main_list = json.load(Clean_Summaries)

# main_url = "https://www.imdb.com/chart/top/"
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
# mainpage = requests.get(main_url, headers=header)
# mainsoup = BeautifulSoup(mainpage.text,'html.parser')
# movie_codes = []
# movies = mainsoup.find_all('li',class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent")
# for movie in movies:
#     movie_code = movie.find('a',class_="ipc-title-link-wrapper")
#     movie_code = re.compile(r"tt\d+").findall(movie_code.attrs["href"])
#     movie_codes.append(movie_code[0])
# with ThreadPoolExecutor() as executor:
#     main_list = list(executor.map(find_summaries, movie_codes))

while True:
    input_summary = input('Enter a movie summary:').lower().strip()
    main_list.append(['input', clean_text(input_summary)])
    print("---Finding Similar Movies---")
    find_similar_movies()
    main_list.pop()
    tfidf_dict.pop('input')
    print("------------")