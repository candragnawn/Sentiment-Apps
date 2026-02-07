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
        print(f"Sentiment AI Engine Active!")
        print(f"Running on: {'GPU (CUDA)' if self.device == 0 else 'CPU'}")
        model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        self.analyzer = pipeline("sentiment-analysis", model=model_name, device=self.device)
        print(f"Running on: {'GPU' if self.device == 0 else 'CPU'}")

    def run_all(self, keyword, days_back=30):
        has_data = self.db.check_existing_keyword(keyword)

        if has_data:
            print(f"Data for '{keyword}' found in database. skipping scrape")
            return {"status": "success", "source": "cache", "message":"Data loaded from database"}
        print(f"No data for '{keyword}'. Starting fresh scrape...")
        with ThreadPoolExecutor() as executor:
            f_news = executor.submit(self.news_scraper.fetch_news, keyword, 1500)
            f_tiktok = executor.submit(self.tiktok_scraper.fetch_tiktok, keyword, 1500)
            f_yt = executor.submit(self.youtube_scraper.search_and_fetch, keyword, 1500)
            f_tweets = executor.submit(self.twitter_scraper.fetch_tweets, keyword, 1500)

            news = f_news.result() or []
            tiktok = f_tiktok.result() or []
            youtube = f_yt.result() or []
            tw_res = f_tweets.result() or {}
            tweets = tw_res.get('tweets', [])
            print(f"DEBUG SCRAPE - News: {len(news)}, TikTok: {len(tiktok)}, YT: {len(youtube)}, Tweets: {len(tweets)}")
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
            total_data = len(valid_texts)
            chunk_size = 50
            all_predictions = []
            print(f"Analyzing {total_data} items in batch...")
            for i in range(0, total_data, chunk_size):
                end_index = min(i + chunk_size, total_data)
                batch = valid_texts[i:end_index]
                
                print(f"⏳ Processing: {i} to {end_index} ({int(end_index/total_data*100)}%)")
              
                batch_preds = self.analyzer(batch, batch_size=16)
                all_predictions.extend(batch_preds)
            for i, item in enumerate(valid_items):
                result = all_predictions[i]
                final_results.append({
                    "keyword": keyword,
                    "platform": item['platform'],
                    "author": item.get('author', 'Unknown'),
                    "text_raw": item['text'],
                    "text_clean": valid_texts[i],
                    "label": result['label'],
                    "score": round(result['score'] * 100, 2),
                    "top_keyword": valid_texts[i].split()[:10],
                    "published_date": item.get('published_date'),
                    "created_at": datetime.now().isoformat()
                })
            if final_results:
                print(f"Menyimpan {len(final_results)} data ke database...")
                success = self.db.save_results(final_results)

                if success:
                    print("Analisis selesai dan data berhasil disimpan!")
                    return {"status": "success", "count": len(final_results)}
                else:
                    print("Gagal menyimpan data ke database.")
                    return {"status": "error", "message": "Database insert failed"}
        return {"status": "no_data", "message": "Tidak ada data valid untuk dianalisis"}