import sys
import os
from pathlib import Path
import asyncio
from functools import lru_cache

sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from database.database_supabase import SentimentDatabase
from typing import List, Optional
from datetime import datetime, timedelta
from contextlib import asynccontextmanager


db = None
analyzer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global analyzer, db
    print("Menyiapkan Database...", flush=True)
    try:
        # Initialize DB in a separate thread if it does heavy setup, though __init__ is usually light.
        # But here we just call it directly as it's just setting up headers.
        db = SentimentDatabase()
        print("Database siap!", flush=True)
    except Exception as e:
        print(f"Gagal memuat Database: {e}", flush=True)
        import traceback
        traceback.print_exc()

    print("Menyiapkan AI Engine (mohon tunggu sebentar)...", flush=True)
    try:
        from core.analyzer import sentimentAnalyzer

        analyzer = sentimentAnalyzer()
        print("AI Engine siap melayani request!", flush=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"AI Engine gagal dimuat: {e}", flush=True)
        analyzer = None
    yield
    print("AI Engine dimatikan.")

app = FastAPI(title="Sentiment Analysis API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"status": "ready", "analyzer_ready": analyzer is not None}

@app.get('/api/sentiment/platform-stats')
async def get_platform_stats(keyword: Optional[str] = None):
    if db is None:
        return []
    try:
        return await asyncio.to_thread(db.fetch_platform_stats, keyword)
    except Exception as e:
        print(f"Error fetching platform stats: {e}")
        return []

@app.get('/api/sentiment/list')
async def get_list(
    keyword: Optional[str] = None,
    days: Optional[int] = Query(None),
    page: int = Query(1),
    page_size: int = Query(500)
):
    if days:
        end = datetime.now()
        start = end - timedelta(days=days)
        return await asyncio.to_thread(db.fetch_data_by_date_range, start, end, keyword)
    
    if db is None:
        return {'data': [], 'total': 0, 'page': page, 'page_size': page_size, 'total_pages': 0}
    
    return await asyncio.to_thread(db.fetch_paginated, page=page, page_size=page_size, keyword=keyword)

@app.get('/api/sentiment/stats')
async def get_stats(keyword: Optional[str] = None):
    if db is None:
        return {"total": 0, "positive": 0, "negative": 0, "neutral": 0}
    return await asyncio.to_thread(db.fetch_stats, keyword)

@app.get('/api/sentiment/chart')
async def get_chart(days: int = Query(30), keyword: Optional[str] = None, group_by: str = Query('day')):
    if db is None:
        return []
    return await asyncio.to_thread(db.fetch_chart_data, days, keyword, group_by)

@app.get('/api/sentiment/history')
async def get_history():
    if db is None:
        return []
    # This function is heavy, so it's good we're threading it.
    # But since `db` is global, we can use an external cache or rely on the OS file cache if it was file based.
    # Since we want to cache the RESULT of this heavy calculation:
    return await asyncio.to_thread(db.fetch_search_history)

@app.get('/api/sentiment/wordcloud')
async def get_wordcloud(keyword: Optional[str] = None):
    if db is None:
        return []
    return await asyncio.to_thread(db.fetch_word_cloud, keyword)

@app.get("/analyze")
async def start_analysis(
    keyword: str, 
    background_tasks: BackgroundTasks, 
    days_back: int = 30,
    max_results: int = 500
):
    if analyzer is None:
        return {"status": "error", "message": "Analyzer belum siap, mohon tunggu sebentar lagi."}
    
    if db:
        analyzer.db = db
    
    # run_all might be blocking too!
    background_tasks.add_task(analyzer.run_all, keyword, days_back, max_results)
    return {"status": "processing", "message": "Analisis dimulai di background"}

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error: {e}", flush=True)



