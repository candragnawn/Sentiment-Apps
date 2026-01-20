from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YouTubeScraper
from scrapping.twitter_scraper import TwitterScraper
from preprocessor import DataCleaner
from database import SentimentDatabase
from transformers import pipeline

class sentimentAnalyzer:
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.youtube_scraper = YouTubeScraper()
        self.twitter_scraper = TwitterScraper()

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
        yt_data = self.youtube_scraper.search_and_fetch(keyword, max_videos=5)
        tweets_res = self.twitter_scraper.fetch_tweets(keyword, limit=50)
        tweets_data = tweets_res['tweets']

        all_raw_data = []
        for n in news_data: all_raw_data.append({'text': n['title'], 'platform': 'News'})
        for y in yt_data: all_raw_data.append({'text': y['text'], 'platform': 'YouTube'})
        for t in tweets_data: all_raw_data.append({'text': t['text'], 'platform': 'Twitter'})
        print(f"collect successfully: {len(all_raw_data)} from 3 platforms")

        print(f"start analyzing and saving to database..")
        for item in all_raw_data:
            cleaned_text = self.cleaner.clean_text(item['text'])

            prediction = self.sentiment_analyzer(cleaned_text)[0]
            label = prediction['label']
            score = round(prediction['score'] * 100, 2)

            self.db.save_result(item['text'], label, score, item['platform'])
        print(f"all data processed and save to database ready to display the keyword: {keyword}")

if __name__ == "__main__":
    system = sentimentAnalyzer()
    target = input("masukan keyword : ")
    system.run_all(target)



