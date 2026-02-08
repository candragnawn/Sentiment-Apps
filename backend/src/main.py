from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from core.analyzer import sentimentAnalyzer
from database.database_supabase import SentimentDatabase
from typing import List, Optional
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))


db = SentimentDatabase()
analyzer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global analyzer
    print("⏳ Menyiapkan AI Engine (mohon tunggu sebentar)...", flush=True)
    try:
        analyzer = sentimentAnalyzer()
        print("AI Engine siap melayani request!", flush=True)
    except Exception as e:
        print(f"Gagal memuat AI Engine: {e}", flush=True)
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
async def get_chart(days: int = Query(30), keyword: Optional[str] = None, group_by: str = Query('day')):
    return db.fetch_chart_data(days, keyword, group_by)

@app.get("/analyze")
async def start_analysis(
    keyword: str, 
    background_tasks: BackgroundTasks, 
    days_back: int = 30  
):
    print(f"DEBUG - Received analysis request for keyword: {keyword}", flush=True)
    if analyzer is None:
        print("DEBUG - Analyzer is still None!", flush=True)
        return {"status": "error", "message": "Analyzer belum siap, mohon tunggu sebentar lagi."}
    
    background_tasks.add_task(analyzer.run_all, keyword, days_back)
    print(f"DEBUG - Task added to background for keyword: {keyword}", flush=True)
    return {"status": "processing", "message": "Analisis dimulai di background"}

if __name__ == "__main__":
    import uvicorn
    # Use the filename directly to avoid double import issues with reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)



