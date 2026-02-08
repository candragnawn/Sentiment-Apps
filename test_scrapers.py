import sys
from pathlib import Path

# Add backend/src to path
sys.path.append(str(Path.cwd() / "backend" / "src"))

from scrapping.scrapper import NewsScraper
from scrapping.youtube_scraper import YoutubeScraper
from scrapping.twitter_scraper import TwitterScraper
from scrapping.tiktok_scraper import TiktokScrapper

def test_scrapers():
    keyword = "Trump"
    
    print("Testing NewsScraper...")
    news = NewsScraper().fetch_news(keyword, limit=5)
    for i, item in enumerate(news):
        print(f"News {i}: Title={item.get('title')[:30]}, Date={item.get('published_date')}")

    print("\nTesting YoutubeScraper...")
    yt = YoutubeScraper().search_and_fetch(keyword, max_videos=5)
    for i, item in enumerate(yt):
        print(f"YouTube {i}: Title={item.get('text')[:30]}, Date={item.get('published_date')}")

    print("\nTesting TiktokScrapper...")
    tt = TiktokScrapper().fetch_tiktok(keyword, limit=5)
    for i, item in enumerate(tt):
        print(f"TikTok {i}: Author={item.get('author')}, Date={item.get('published_date')}")

    print("\nTesting TwitterScraper...")
    tw_res = TwitterScraper().fetch_tweets(keyword, limit=5)
    tweets = tw_res.get('tweets', [])
    for i, t in enumerate(tweets[:5]):
        raw_date = t.get('legacy', {}).get('created_at')
        print(f"Twitter {i}: Raw Date={raw_date}")

if __name__ == "__main__":
    test_scrapers()
