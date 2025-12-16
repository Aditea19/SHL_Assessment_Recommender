import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load embeddings and data
with open("data/embeddings.pkl", "rb") as f:
    saved_data = pickle.load(f)

embeddings = saved_data["embeddings"]
data = saved_data["data"]

# Load the same model used for embeddings
model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def search_assessments(query, top_k=5):
    # Convert query to embedding
    model = get_model()
    query_embedding = model.encode([query])


    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # Get top-k indices
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
