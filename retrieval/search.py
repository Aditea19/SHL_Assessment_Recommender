import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
with open("data/embeddings.pkl", "rb") as f:
    saved_data = pickle.load(f)

data = saved_data["data"]

# Build corpus from assessment names
corpus = data["name"].tolist()

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(corpus)

def search_assessments(query, top_k=5):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "name": data.iloc[idx]["name"],
            "url": data.iloc[idx]["url"],
            "score": round(float(similarities[idx]), 3)
        })

    return results



if __name__ == "__main__":
    user_query = input("Enter your requirement: ")
    results = search_assessments(user_query)

    print("\nTop matching assessments:\n")
    for r in results:
        print(f"{r['name']}  |  score: {r['score']}")
        print(f"{r['url']}\n")
