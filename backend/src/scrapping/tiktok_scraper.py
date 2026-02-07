import requests
from datetime import datetime

class TiktokScrapper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://scraptik.p.rapidapi.com/search-posts"
        self.host = "scraptik.p.rapidapi.com"
    
    def fetch_tiktok(self, keyword, limit=500, publish_time=0):
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        params = {
            "keyword": keyword,
            "count": str(limit),
            "offset": "0",
            "use_filters": "0",
            "publish_time": str(publish_time),
            "region": "ID"
        }
        try:
            response = requests.get(self.url, headers=headers, params=params, timeout=15)
            if response.status_code != 200:
                return []
            
            data = response.json()
            raw = data.get('data', {}).get('aweme_list') or data.get('aweme_list') or []
            
            if not raw and 'search_item_list' in data:
                raw = [i.get('aweme_info') for i in data['search_item_list'] if i.get('aweme_info')]
            
            results = []
            for post in raw:
                caption = post.get('desc')
                if caption:
                    ts = post.get('create_time', 0)
                    results.append({
                        'text': caption,
                        'author': post.get('author', {}).get('nickname'),
                        'platform': 'TikTok',
                        'published_date': datetime.fromtimestamp(ts).isoformat() if ts else None
                    })
            return results
        except Exception:
            return []

