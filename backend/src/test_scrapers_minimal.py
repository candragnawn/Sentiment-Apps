import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from scrapping.tiktok_scraper import TiktokScrapper
from scrapping.scrapper import NewsScraper

async def test_scrapers():
    keyword = "prabowo"
    limit = 5
    
    print(f"Testing scrapers with keyword: {keyword}, limit: {limit}")
    
    # News
    print("\n--- Testing News ---")
    news = NewsScraper()
    news_res = news.fetch_news(keyword, limit=limit)
    print(f"News results (count={len(news_res)}):")
    for r in news_res[:2]:
        print(f" - {r.get('title')[:50]}...")

    # YouTube
    print("\n--- Testing YouTube ---")
    yt = YoutubeScraper()
    yt_res = yt.search_and_fetch(keyword, max_videos=limit)
    print(f"YouTube results (count={len(yt_res)}):")
    for r in yt_res[:2]:
        print(f" - {r.get('text')[:50]}...")

    # Twitter
    print("\n--- Testing Twitter ---")
    twitter = TwitterScraper()
    tw_res = twitter.fetch_tweets(keyword, limit=limit)
    tweets = tw_res.get('tweets', [])
    print(f"Twitter results (count={len(tweets)}):")
    for r in tweets[:2]:
        print(f" - {r.get('text')[:50]}...")

    # TikTok
    print("\n--- Testing TikTok ---")
    tiktok = TiktokScrapper()
    tk_res = tiktok.fetch_tiktok(keyword, limit=limit)
    print(f"TikTok results (count={len(tk_res)}):")
    for r in tk_res[:2]:
        print(f" - {r.get('text')[:50]}...")

if __name__ == "__main__":
    asyncio.run(test_scrapers())
