
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from core.analyzer import sentimentAnalyzer
from database.database_supabase import SentimentDatabase
import uvicorn
from typing import List

app = FastAPI(title="Sentiment Analysis API")
db = SentimentDatabase()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
analyzer =sentimentAnalyzer()

@app.get('/api/sentiment/list')
async def get_stats():
  
       data = db.fetch_all_data()
       return data

@app.get("/")
def read_root():
    return {"status": "backend sentiment is ready"}



@app.get("/analyze")
async def start_analysis(keyword: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(analyzer.run_all, keyword)
    return {
        "message" : f"analysis for '{keyword}' has been started in background",
        "status" : f"processing"
    }
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


