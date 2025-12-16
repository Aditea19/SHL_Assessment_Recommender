import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from retrieval.search import search_assessments

DATASET_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_CSV = "aditi_arya.csv"  # change name if needed

df = pd.read_excel(DATASET_PATH)

rows = []

for _, row in df.iterrows():
    query = row["Query"]

    results = search_assessments(query, top_k=5)

    rows.append({
        "query": query,
        "prediction_1": results[0]["url"] if len(results) > 0 else "",
        "prediction_2": results[1]["url"] if len(results) > 1 else "",
        "prediction_3": results[2]["url"] if len(results) > 2 else "",
        "prediction_4": results[3]["url"] if len(results) > 3 else "",
        "prediction_5": results[4]["url"] if len(results) > 4 else "",
    })

pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False)
print(f"Saved predictions to {OUTPUT_CSV}")
