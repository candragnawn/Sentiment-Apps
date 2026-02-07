
import sys
import os
from pathlib import Path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from core.analyzer import sentimentAnalyzer
from database.database_supabase import SentimentDatabase
import uvicorn
from typing import List, Optional
from datetime import datetime, timedelta

app = FastAPI(title="Sentiment Analysis API")
db = SentimentDatabase()
analyzer = sentimentAnalyzer()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ready"}

@app.get('/api/sentiment/list')
async def get_list(
    keyword: Optional[str] = None,
    days: Optional[int] = Query(None),
    page: int = Query(1),
    page_size: int = Query(100)
):
    if days:
        end = datetime.now()
        start = end - timedelta(days=days)
        return db.fetch_data_by_date_range(start, end, keyword)
    
    return db.fetch_paginated(page=page, page_size=page_size, keyword=keyword)

@app.get('/api/sentiment/stats')
async def get_stats(keyword: Optional[str] = None):
    return db.fetch_stats(keyword)

@app.get('/api/sentiment/chart')
async def get_chart(days: int = Query(30), keyword: Optional[str] = None):
    return db.fetch_chart_data(days, keyword)

@app.get("/analyze")
async def start_analysis(
    keyword: str, 
    background_tasks: BackgroundTasks, 
    days_back: int = 30  
):
    background_tasks.add_task(analyzer.run_all, keyword, days_back)
    return {"status": "processing", "message": "Analisis dimulai di background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



