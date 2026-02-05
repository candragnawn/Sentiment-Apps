from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from scrapping.tiktok_scraper import TiktokScrapper
from core.preprocessor import DataCleaner
from database.database_supabase import SentimentDatabase
from transformers import pipeline
from datetime import datetime
import dateparser

class sentimentAnalyzer:
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.youtube_scraper = YoutubeScraper()
        self.twitter_scraper = TwitterScraper()
        self.tiktok_scraper = TiktokScrapper()
        self.cleaner = DataCleaner()
        self.db = SentimentDatabase()
        
        model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        self.analyzer = pipeline("sentiment-analysis", model=model_name)

    def run_all(self, keyword, days_back=30):
        has_data = self.db.check_excisting_keyword(keyword)

        if has_data:
            print(f"Data for '{keyword}' found in database. skipping scrape")
            return {"status": "success", "source": "cache", "message":"Data loaded from database"}
        print(f"No data for '{keyword}'. Starting fresh scrape...")
        # self.db.hapus_semua_data()
        
        news = self.news_scraper.fetch_news(keyword, limit=500)
        tiktok = self.tiktok_scraper.fetch_tiktok(keyword, limit=500)
        youtube = self.youtube_scraper.search_and_fetch(keyword, max_videos=500)
        tweets = self.twitter_scraper.fetch_tweets(keyword, limit=500).get('tweets', [])

        processed_data = []
        
        for item in news:
            processed_data.append({
                'text': item['title'], 
                'platform': 'News',
                'published_date': item.get('published_date')
            })
            
        for item in youtube:
            processed_data.append({
                'text': item['text'], 
                'platform': 'YouTube',
                'published_date': item.get('published_date')
            })
            
        for t in tweets:
            text = t.get('legacy', {}).get('full_text') or t.get('text')
            if not text: continue
            
            pub_date = None
            raw_date = t.get('legacy', {}).get('created_at')
            if raw_date:
                try:
                    pub_date = dateparser.parse(raw_date).isoformat()
                except:
                    pass

            author = 'Unknown'
            try:
                author = t.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {}).get('screen_name', 'Unknown')
            except:
                pass
                
            processed_data.append({
                'text': text, 
                'platform': 'Twitter',
                'author': author,
                'published_date': pub_date
            })
            
        for t in tiktok:
            if t.get('text'):
                processed_data.append({
                    'text': t['text'],
                    'platform': 'TikTok',
                    'author': t.get('author', 'User Tiktok'),
                    'published_date': t.get('published_date')
                })

        final_results = []
        all_clean_text = [self.cleaner.clean_text(item['text']) for item in processed_data]
        valid_items = [item for i, item in enumerate(processed_data) if all_clean_text[i]]
        valid_texts = [t for t in all_clean_text if t]

        if valid_texts:
            print(f"Analyzing {len(valid_texts)} items in batch...")
            predictions = self.analyzer(valid_texts, batch_size=16)
            for i, item in enumerate(valid_items):
                result = predictions[i]
                final_results.append({
                    "keyword": keyword,
                    "platform": item['platform'],
                    "author": item.get('author', 'Unknown'),
                    "text_raw": item['text'],
                    "text_clean": valid_texts[i],
                    "label": result['label'],
                    "score": round(result['score'] * 100, 2),
                    "top_keyword": valid_texts[i].split()[:100],
                    "published_date": item.get('published_date'),
                    "created_at": datetime.now().isoformat()
                })
            if final_results:
                chunk_size = 100