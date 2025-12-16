import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

df = pd.read_csv("data/shl_assessments_raw.csv")


texts = []

for _, row in df.iterrows():
    combined_text = f"{row['name']}. {row['description']}"
    texts.append(combined_text)


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(texts, show_progress_bar=True)

with open("data/embeddings.pkl", "wb") as f:
    pickle.dump({
        "embeddings": embeddings,
        "data": df
    }, f)

print("Embeddings created and saved.")
