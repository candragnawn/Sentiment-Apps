import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import random
import re

class sentimentAnalyzer:
    
    def __init__(self):
        from scrapping.scrapper import NewsScraper
        from scrapping.youtube_scraper import YoutubeScraper
        from scrapping.twitter_scraper import TwitterScraper
        from scrapping.tiktok_scraper import TiktokScrapper
        from core.preprocessor import DataCleaner
        from database.database_supabase import SentimentDatabase
        
        self.news_scraper = NewsScraper()
        self.youtube_scraper = YoutubeScraper()
        self.twitter_scraper = TwitterScraper()
        self.tiktok_scraper = TiktokScrapper()
        self.cleaner = DataCleaner()
        self.db = SentimentDatabase()
        
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best',
            'happy', 'perfect', 'awesome', 'brilliant', 'beautiful', 'nice', 'super', 'incredible',
            'outstanding', 'terrific', 'fabulous', 'marvelous', 'superb', 'delightful', 'pleasant',
            'bagus', 'hebat', 'luar biasa', 'sempurna', 'mantap', 'keren', 'suka', 'senang',
            'bahagia', 'indah', 'cantik', 'positif', 'sukses', 'berhasil', 'memuaskan'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor', 'disappointing',
            'sad', 'angry', 'annoying', 'frustrating', 'disgusting', 'pathetic', 'useless',
            'fail', 'failed', 'failure', 'problem', 'issue', 'broken', 'wrong', 'error',
            'buruk', 'jelek', 'mengecewakan', 'gagal', 'kecewa', 'marah', 'sedih', 'benci',
            'payah', 'rusak', 'salah', 'negatif', 'masalah', 'tidak suka', 'kurang'
        }
        
        print(f"Sentiment AI Engine Active! (Rule-based mode)", flush=True)
        print(f"Running on: CPU (no ML dependencies)", flush=True)

    def analyze_sentiment(self, text):
        try:
            text_lower = text.lower()
            words = re.findall(r'\b\w+\b', text_lower)
            
            positive_count = sum(1 for word in words if word in self.positive_words)
            negative_count = sum(1 for word in words if word in self.negative_words)
            
            total_sentiment_words = positive_count + negative_count
            
            if total_sentiment_words == 0:
                label = "neutral"
                score = 50.0
            else:
                positive_ratio = positive_count / total_sentiment_words
                score = positive_ratio * 100
                
                if score > 60:
                    label = "positive"
                elif score < 40:
                    label = "negative"
                else:
                    label = "neutral"
            
            return {
                "label": label,
                "score": score
            }
        except:
            return {"label": "neutral", "score": 50.0}

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
            
            if platform == 'News':
                initial_date = item.get('published_date') or datetime.now().isoformat()
            else:
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
        for p in processed:
            res = self.analyze_sentiment(p['text_clean'])
            final_results.append({
                "keyword": keyword,
                "platform": p['platform'],
                "author": p['author'],
                "text_raw": p['text_raw'],
                "text_clean": p['text_clean'],
                "label": res['label'],
                "score": round(res['score'], 2),
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
