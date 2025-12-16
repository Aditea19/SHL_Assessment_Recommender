import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from retrieval.search import search_assessments

DATASET_PATH = "data/Gen_AI Dataset.xlsx"

def evaluate(top_k_values=[1, 3, 5]):
    df = pd.read_excel(DATASET_PATH)

    total = len(df)
    hits = {k: 0 for k in top_k_values}

    for _, row in df.iterrows():
        query = row["Query"]
        true_url = row["Assessment_url"]

        results = search_assessments(query, top_k=max(top_k_values))
        predicted_urls = [r["url"] for r in results]

        for k in top_k_values:
            if true_url in predicted_urls[:k]:
                hits[k] += 1

    print("Evaluation Results")
    print("------------------")
    for k in top_k_values:
        accuracy = hits[k] / total if total > 0 else 0
        print(f"Recall@{k}: {accuracy:.2f}")

if __name__ == "__main__":
    evaluate()
