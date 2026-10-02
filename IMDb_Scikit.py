import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_movies():
    vectorizer = TfidfVectorizer(stop_words="english")
    summaries = [movie[1] for movie in main_list]
    tfidf_matrix = vectorizer.fit_transform(summaries)
    input_vector = tfidf_matrix[-1].toarray().flatten()
    similarity_scores = (cosine_similarity([input_vector], tfidf_matrix[:-1])).flatten()
    similarity_list = []
    for i, score in enumerate(similarity_scores):
        similarity_list.append((main_list[i][0], round(score, 4)))
    final_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)
    for i in range(5):
        print(final_list[i][0])

main_list = []
with open("Clean_Summaries.json", "r") as Clean_Summaries:
    main_list = json.load(Clean_Summaries)

while True:
    input_summary = input('Enter a movie summary:').lower().strip()
    main_list.append(['input', input_summary])
    print("---Finding Similar Movies---")
    find_similar_movies()
    main_list.pop()
    print("------------")