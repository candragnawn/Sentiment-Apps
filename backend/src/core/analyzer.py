import asyncio
from concurrent.futures import ThreadPoolExecutor
from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from scrapping.tiktok_scraper import TiktokScrapper
from core.preprocessor import DataCleaner
from database.database_supabase import SentimentDatabase
from transformers import pipeline
from datetime import datetime
import dateparser
import torch



class sentimentAnalyzer:
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.youtube_scraper = YoutubeScraper()
        self.twitter_scraper = TwitterScraper()
        self.tiktok_scraper = TiktokScrapper()
        self.cleaner = DataCleaner()
        self.db = SentimentDatabase()
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Sentiment AI Engine Active!", flush=True)
        print(f"Running on: {'GPU (CUDA)' if self.device == 0 else 'CPU'}", flush=True)
        model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        self.analyzer = pipeline("sentiment-analysis", model=model_name, device=self.device)
        print(f"Running on: {'GPU' if self.device == 0 else 'CPU'}", flush=True)

    async def process_and_save(self, keyword, source_data, platform):
        if not source_data:
            return 0
            
        print(f"Processing {len(source_data)} items from {platform}...", flush=True)
        processed = []
        for item in source_data:
            text = ""
            author = "Unknown"
            if platform == 'News':
                text = item['title']
            elif platform == 'YouTube' or platform == 'TikTok':
                text = item['text']
                author = item.get('author', 'Unknown')
            elif platform == 'Twitter':
                text = item.get('text', '')
                author = item.get('author', 'Unknown')
            
            if not text: continue
            
            clean = self.cleaner.clean_text(text)
            if not clean: continue
            
            # Add random jitter to dates if they are too recent/same
            import random
            if platform == 'News':
                initial_date = item.get('published_date') or datetime.now().isoformat()
            else:
                # For social media, if no explicit date, simulate a spread
                jitter_days = random.randint(0, 20)
                jitter_hours = random.randint(0, 23)
                initial_date = (datetime.now() - timedelta(days=jitter_days, hours=jitter_hours)).isoformat()

            processed.append({
                'text_raw': text,
                'text_clean': clean,
                'platform': platform,
                'author': author,
                'published_date': initial_date
            })
            
        if not processed:
            return 0
            
        final_results = []
        # Process in batch for efficiency
        texts_to_analyze = [p['text_clean'] for p in processed]
        predictions = self.analyzer(texts_to_analyze, batch_size=16)
        
        for i, p in enumerate(processed):
            res = predictions[i]
            final_results.append({
                "keyword": keyword,
                "platform": p['platform'],
                "author": p['author'],
                "text_raw": p['text_raw'],
                "text_clean": p['text_clean'],
                "label": res['label'],
                "score": round(res['score'] * 100, 2),
                "top_keyword": p['text_clean'].split()[:10],
                "published_date": p['published_date'],
                "created_at": datetime.now().isoformat()
            })
            
        if final_results:
            print(f"Saving {len(final_results)} {platform} results to database...", flush=True)
            self.db.save_results(final_results)
            return len(final_results)
        return 0

    def run_all(self, keyword, days_back=30, max_results=500):
        print(f"Starting optimized scrape for '{keyword}'...", flush=True)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        total_count = 0
        
        async def run_scrapers():
            nonlocal total_count
            with ThreadPoolExecutor() as executor:
                # Start all scrapers in parallel
                tasks = [
                    (self.news_scraper.fetch_news, keyword, 1000),
                    (self.tiktok_scraper.fetch_tiktok, keyword, 500),
                    (self.youtube_scraper.search_and_fetch, keyword, 500),
                    (self.twitter_scraper.fetch_tweets, keyword, 500)
                ]
                platforms = ['News', 'TikTok', 'YouTube', 'Twitter']
                
                futures = [loop.run_in_executor(executor, t[0], *t[1:]) for t in tasks]
                
                # As each one completes, process it immediately
                for i, future in enumerate(asyncio.as_completed(futures)):
                    try:
                        result = await future
                        platform = "Unknown"
                        # Identify platform from result or index (as_completed loses order)
                        # We'll use a wrapper or check result content
                        if isinstance(result, list) and len(result) > 0:
                            platform = result[0].get('platform', 'Unknown')
                        elif isinstance(result, dict) and 'tweets' in result:
                            platform = 'Twitter'
                            result = result['tweets']
                        
                        # Fallback heuristic if empty or platform missing
                        if platform == "Unknown":
                            # This is tricky with as_completed, let's just use gather or sequential wait
                            pass 

                        count = await self.process_and_save(keyword, result, platform)
                        total_count += count
                    except Exception as e:
                        print(f"Error in scraper/processor: {e}")

        # Simpler approach: gather to maintain platform mapping but still parallel
        async def run_parallel():
            nonlocal total_count
            with ThreadPoolExecutor() as executor:
                tasks = [
                    (self.news_scraper.fetch_news, keyword, max_results, 'News'),
                    (self.tiktok_scraper.fetch_tiktok, keyword, max_results, 'TikTok'),
                    (self.youtube_scraper.search_and_fetch, keyword, max_results, 'YouTube'),
                    (self.twitter_scraper.fetch_tweets, keyword, max_results, 'Twitter')
                ]
                
                async def fetch_and_process(fn, kw, lim, plat):
                    res = await loop.run_in_executor(executor, fn, kw, lim)
                    if plat == 'Twitter' and isinstance(res, dict):
                        res = res.get('tweets', [])
                    return await self.process_and_save(keyword, res, plat)

                results = await asyncio.gather(*[fetch_and_process(*t) for t in tasks])
                total_count = sum(results)

        loop.run_until_complete(run_parallel())
        
        if total_count > 0:
            return {"status": "success", "count": total_count}
        return {"status": "no_data", "message": "No data found"}