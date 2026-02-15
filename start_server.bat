@echo off
echo Starting Sentiment Analysis Backend (Production Mode)...
cd backend/src
:: Run Uvicorn with 4 workers for better concurrency
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
pause
