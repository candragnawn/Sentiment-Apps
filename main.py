from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from preprocessor import DataCleaner
from database_supabase import SentimentDatabase
from transformers import pipeline
from scrapping.tiktok_scraper import TiktokScrapper

class sentimentAnalyzer:
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.youtube_scraper = YoutubeScraper()
        self.twitter_scraper = TwitterScraper()
        self.tiktok_scraper = TiktokScrapper()

        self.cleaner = DataCleaner()
        self.db = SentimentDatabase()

        print('loading model..')
        model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

    def run_all(self, keyword):
        self.db.hapus_semua_data()
        print(f"start operating for keyword: {keyword}")
        # data collect
        news_data = self.news_scraper.fetch_news(keyword)
        tiktok_data = self.tiktok_scraper.fetch_tiktok(keyword)
        yt_data = self.youtube_scraper.search_and_fetch(keyword, max_videos=5)
        tweets_res = self.twitter_scraper.fetch_tweets(keyword, limit=50)
        tweets_data = tweets_res.get('tweets', [])

        all_raw_data = []
        for n in news_data: all_raw_data.append({'text': n['title'], 'platform': 'News'})
        for y in yt_data: all_raw_data.append({'text': y['text'], 'platform': 'YouTube'})
        for t in tweets_data:
           raw_text = (
                t.get('legacy', {}).get('full_text') or 
                t.get('core', {}).get('metadata', {}).get('text') or
                t.get('text')
            )
           if raw_text:
               
                screen_name = 'Unknown'
                try:
                    screen_name = t.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {}).get('screen_name', 'Unknown')
                except: pass
                all_raw_data.append({
                    'text': raw_text, 
                    'platform': 'Twitter',
                    'author': screen_name
                })
        for t in tiktok_data:
            text = t.get('title') or t.get('description')
            if text:
                all_raw_data.append({
                    'text': text,
                    'platform': 'TikTok',
                    'author': t.get('author', {}).get('nickname', 'User TikTok')
                })
        print(f"collect successfully: {len(all_raw_data)} from 3 platforms")

        print(f"start analyzing and saving to database..")
        for item in all_raw_data:
            cleaned_text = self.cleaner.clean_text(item['text'])
            if not cleaned_text: continue

            prediction = self.sentiment_analyzer(cleaned_text)[0]
            label = prediction['label']
            score = round(prediction['score'] * 100, 2)

            data_supabase = {
                "keyword": keyword,
                "platform": item['platform'],
                "author": item.get('author', 'Unknown'),
                "text_raw": item['text'],
                "text_clean": cleaned_text,
                "label": label,
                "score": score,
                "top_keyword": cleaned_text.split()[:10]

            }
            self.db.save_results(data_supabase)
        print(f"all data processed and save to database ready to display the keyword: {keyword}")

if __name__ == "__main__":
    system = sentimentAnalyzer()
    target = input("masukan keyword : ")
    system.run_all(target)



