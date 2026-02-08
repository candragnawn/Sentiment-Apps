import sys
from pathlib import Path
sys.path.append(str(Path.cwd() / "backend" / "src"))
from scrapping.youtube_scraper import YoutubeScraper

yt = YoutubeScraper().search_and_fetch("indonesia", max_videos=5)
for i, item in enumerate(yt):
    print(f"YouTube {i}: Title={item.get('text')[:30]}, Date={item.get('published_date')}")
