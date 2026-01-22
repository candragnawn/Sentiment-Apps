import requests
from bs4 import BeautifulSoup

class NewsScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
    def fetch_news(self, keyword):
        import urllib.parse
        encoded = urllib.parse.quote_plus(keyword)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=id&gl=ID&ceid=ID:id"
        articles = []

        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, features="xml")
            items = soup.find_all('item')

            for item in items:
                try:
                    title = item.title.text if item.title else "no title"
                    desc_tag = item.find('description')
                    snippet = desc_tag.text if desc_tag else ""
                    clean_snippet = BeautifulSoup(snippet, "html.parser").get_text()

                    articles.append({
                        'title' : title,
                        'snippet' : clean_snippet
                    })
                except Exception:
                    continue
            return articles

        except Exception as e:
            print(f"Error: {e}")
            return []