from fastapi import FastAPI, Query
from retrieval.search import search_assessments

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API to recommend SHL assessments based on text queries",
    version="1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/search")
def search(query: str = Query(..., description="Text describing required skills")):
    results = search_assessments(query)
    return {
        "query": query,
        "results": results
    }
