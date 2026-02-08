import sys
import os
from pathlib import Path

# Fix path for imports
sys.path.append(str(Path.cwd() / 'backend' / 'src'))

from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from scrapping.tiktok_scraper import TiktokScrapper

def test_keyword(keyword):
    print(f"\n--- Testing Keyword: {keyword} ---")
    
    # News
    print("Testing News...")
    news = NewsScraper().fetch_news(keyword, limit=50)
    print(f"News results: {len(news)}")
    
    # YouTube
    print("Testing YouTube...")
    yt = YoutubeScraper().search_and_fetch(keyword, max_videos=10)
    print(f"YouTube results: {len(yt)}")
    if yt:
        print(f"Sample YT Date: {yt[0].get('published_date')}")
    
    # TikTok
    print("Testing TikTok...")
    tiktok = TiktokScrapper().fetch_tiktok(keyword, limit=10)
    print(f"TikTok results: {len(tiktok)}")
    if tiktok:
        print(f"Sample TikTok Date: {tiktok[0].get('published_date')}")

    # Twitter
    print("Testing Twitter...")
    tw_res = TwitterScraper().fetch_tweets(keyword, limit=10)
    tweets = tw_res.get('tweets', [])
    print(f"Twitter results: {len(tweets)}")

if __name__ == "__main__":
    test_keyword("Bigmo")
    test_keyword("Trump")
