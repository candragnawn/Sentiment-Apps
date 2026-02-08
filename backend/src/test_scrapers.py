from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from scrapping.tiktok_scraper import TiktokScrapper
import json

def test_scrapers():
    keyword = "Prabowo"
    print(f"Testing scrapers for keyword: {keyword}")
    
    # Test News
    print("\n--- Testing News ---")
    news = NewsScraper().fetch_news(keyword, limit=5)
    print(f"News items fetched: {len(news)}")
    if news: print(f"Sample news: {news[0].get('title')}")
    
    # Test YouTube
    print("\n--- Testing YouTube ---")
    yt = YoutubeScraper().search_and_fetch(keyword, max_videos=5)
    print(f"YouTube items fetched: {len(yt)}")
    if yt: print(f"Sample YouTube: {yt[0].get('text')[:50]}...")
    
    # Test Twitter
    print("\n--- Testing Twitter ---")
    tw = TwitterScraper().fetch_tweets(keyword, limit=5)
    tweets = tw.get('tweets', [])
    print(f"Twitter items fetched: {len(tweets)}")
    
    # Test TikTok
    print("\n--- Testing TikTok ---")
    tk = TiktokScrapper().fetch_tiktok(keyword, limit=5)
    print(f"TikTok items fetched: {len(tk)}")

if __name__ == "__main__":
    test_scrapers()
