import requests
import json


class TiktokScrapper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://scraptik.p.rapidapi.com/search-posts"
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
            "offset": "0",
            "use_filters": "0",
            "publish_time": "0",
            "sort_type": "0",
            "region": "ID"
        }
        try:
            response = requests.get(self.url, headers=headers, params=querystring, timeout=15)
        
            if response.status_code != 200:
                print(f"API Error: Status {response.status_code}")
                print(f"Response: {response.text}")
                return []
            
            data = response.json()
            
            raw_posts = data.get('data', {}).get('aweme_list') or data.get('aweme_list') or data.get('posts') or []
            
            if not raw_posts and 'search_item_list' in data:
                search_items = data.get('search_item_list', [])
                raw_posts = [item.get('aweme_info') for item in search_items if item.get('aweme_info')]
            
            if not raw_posts:
                print(f"No posts found. Checking aweme_list length: {len(data.get('aweme_list', []))}")
                print(f"Checking search_item_list length: {len(data.get('search_item_list', []))}")
                print(f"Available keys: {data.keys()}")
                return []
            
            print(f"Found {len(raw_posts)} posts to process")
            
            final_data = []
            for post in raw_posts:
                caption = post.get('desc') if post else None
                if caption:
                    final_data.append({
                        'text': caption,
                        'author': post.get('author', {}).get('nickname') if post else None,
                        'platform': 'TikTok'
                    })
            
            print(f"Berhasil menarik {len(final_data)} data dari TikTok!")
            return final_data
            
        except requests.exceptions.Timeout:
            print(f"TikTok Error: Request timeout - API may be down or your key is invalid")
            return []
        except requests.exceptions.ConnectionError:
            print(f"TikTok Error: Connection error - check your internet or API endpoint")
            return []
        except Exception as e:
            print(f"TikTok Error: {e}")
            return []