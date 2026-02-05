import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import dateparser
import urllib.parse

class NewsScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_news(self, keyword, limit=500, days_back=30):
        encoded = urllib.parse.quote_plus(keyword)
        url = f"https://news.google.com/rss/search?q={encoded}+when:{days_back}d&hl=id&gl=ID&ceid=ID:id"
        
        articles = []
        cutoff = datetime.now() - timedelta(days=days_back)

        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, features="xml")
            items = soup.find_all('item')

            for item in items:
                try:
                    title = item.title.text if item.title else "no title"
                    snippet = item.find('description').text if item.find('description') else ""
                    clean_snippet = BeautifulSoup(snippet, "html.parser").get_text()
                    
                    pub_date_str = item.find('pubDate').text if item.find('pubDate') else None
                    pub_date = dateparser.parse(pub_date_str) if pub_date_str else None
                    
                    if pub_date and pub_date < cutoff:
                        continue

                    articles.append({
                        'title': title,
                        'snippet': clean_snippet,
                        'published_date': pub_date.isoformat() if pub_date else None
                    })
                except:
                    continue
            return articles
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []