# AI-Driven Sentiment Analysis Dashboard

A robust, full-stack application designed to aggregate, analyze, and visualize public sentiment across multiple social media and news platforms in real-time. This project leverages distributed scraping, machine learning (DistilBERT), and a high-performance interactive frontend to deliver actionable insights.

---

## Key Features

- **Multi-Platform Data Aggregation**: Real-time scraping from X (Twitter), TikTok, YouTube, and Google News.
- **Advanced AI Engine**: Powered by a multilingual DistilBERT model for high-accuracy sentiment classification (Positive, Negative, Neutral).
- **Interactive Analytics**: Dynamic data visualization using Next.js and Recharts, featuring interactive trend lines, distribution charts, and word clouds.
- **High Performance**: Asynchronous background task processing using FastAPI to handle long-running scraping jobs without blocking the UI.
- **Cloud Database**: Scalable data storage and real-time synchronization with Supabase.
- **Responsive UI**: A premium, glassmorphism-inspired dashboard that is fully responsive across mobile and desktop devices.

---

## Technology Stack

### Backend (Intelligence & Scraping)
- **Python / FastAPI**: High-performance REST API.
- **PyTorch & Transformers**: Multilingual DistilBERT model for NLP processing.
- **Asynchronous Processing**: Parallel scraping using asyncio and ThreadPoolExecutor.
- **yt-dlp**: Automated metadata extraction from video platforms.
- **Supabase (PostgreSQL)**: Relational data storage with optimized indexing for keyword search.

### Frontend (Visualization)
- **Next.js 15+ & React**: Modern, server-side rendered application framework.
- **Tailwind CSS**: Utility-first styling with custom glassmorphism components.
- **Recharts**: Highly interactive and responsive SVG-based charting.
- **Lucide React**: Icons for UI components.

---

## System Architecture

1.  **Request Layer**: The user enters a keyword in the Next.js frontend.
2.  **Orchestrator**: The FastAPI backend receives the request and spawns independent scraper tasks.
3.  **Extraction**: Multiple platform-specific scrapers (Twitter API, TikTok API, Google News RSS, yt-dlp) fetch raw data in parallel.
4.  **AI Analysis**: The SentimentAnalyzer cleans the text and runs it through the machine learning model.
5.  **Persistence**: Results are batched and synced to Supabase.
6.  **Visualization**: The frontend fetches the analyzed data and dynamically updates charts, stats, and the word cloud.

---

## Technical Highlights

This project demonstrates several advanced software engineering concepts:
- **Optimization**: Refactored to remove data caps and implemented batch processing for database operations, increasing throughput significantly.
- **Error Resilience**: Implemented robust error handling for external APIs with fallback mechanisms and exponential backoff.
- **Concurrency**: Leveraged Python's asyncio to reduce data collection time by parallelizing requests across multiple remote sources.
- **Clean Architecture**: Separated concerns between core AI logic, database abstractions, and platform-specific scraping modules.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase Account

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/candragnawn/Sentiment-Apps.git
    cd Sentiment-Apps
    ```
2.  **Backend Setup**:
    ```bash
    cd backend
    pip install -r requirements.txt
    python src/main.py
    ```
3.  **Frontend Setup**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## Contact

**Candra** - [Your LinkedIn/Portfolio Link]

*Project Link: [https://github.com/candragnawn/Sentiment-Apps](https://github.com/candragnawn/Sentiment-Apps)*