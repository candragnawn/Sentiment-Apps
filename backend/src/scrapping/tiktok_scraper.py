import requests
from datetime import datetime

class TiktokScrapper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://tiktok-api23.p.rapidapi.com/api/search/general"
        self.host = "tiktok-api23.p.rapidapi.com"
    
    def fetch_tiktok(self, keyword, limit=500, publish_time=0):
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        
        all_results = []
        cursor = 0 
        
        while len(all_results) < limit:
            params = {
                "keyword": keyword,
                "count": "20", 
                "cursor": str(cursor),
                "publish_time": str(publish_time),
                "region": "ID"
            }
            try:
                response = requests.get(self.url, headers=headers, params=params, timeout=15)
                if response.status_code != 200:
                    print(f"TikTok API Error: {response.status_code} - {response.text}", flush=True)
                    break
                
                data = response.json()
                
    
                raw_data = data.get('data', [])
                if not raw_data:
                    break
                
                page_results = []
                for entry in raw_data:
                    item = entry.get('item', {})
                    caption = item.get('desc')
                    if caption:
                        ts = item.get('createTime', 0)
                        author = item.get('author', {}).get('nickname', 'User Tiktok')
                        page_results.append({
                            'text': caption,
                            'author': author,
                            'platform': 'TikTok',
                            'published_date': datetime.fromtimestamp(ts).isoformat() if ts else None
                        })
                
                all_results.extend(page_results)
                
                new_cursor = data.get('cursor')
                if new_cursor == cursor or not new_cursor:
                    break
                cursor = new_cursor

                if len(raw_data) < 5:
                    break
                    
            except Exception as e:
                print(f"TikTok Scraper Exception: {e}", flush=True)
                break
                
        return all_results[:limit]

