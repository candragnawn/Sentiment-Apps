import requests

class TiktokScrapper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://scraptik.p.rapidapi.com/search/video"
        self.host = "scraptik.p.rapidapi.com"
    def fetch_tiktok(self, keyword, limit=30):
        print(f"Tiktok: mencari konten untuk: '{keyword}'...")
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        querystring = {
            "keyword": keyword, 
            "count": str(limit),
            "cursor": "0"
        }
        try:
            response = requests.get(self.url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            posts = (
                data.get('aweme_list') or 
                data.get('data', {}).get('videos') or 
                data.get('data', [])
            )
            
            if isinstance(data, list):
                posts = data
                print(f"Berhasil menarik {len(posts)} data dari TikTok!")
            return posts
        except Exception as e:
            print(f"TikTok Error: {e}")
            return []