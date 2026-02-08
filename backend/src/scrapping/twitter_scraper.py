import requests

class TwitterScraper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://twitter-api47.p.rapidapi.com/v3/search" 
        self.host = "twitter-api47.p.rapidapi.com"

    def fetch_tweets(self, keyword, limit=500):
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        
        all_tweets = []
        cursor = None
        
        print(f"DEBUG: Starting Twitter scrape for '{keyword}' limit {limit}", flush=True)

        while len(all_tweets) < limit:
            params = {
                "query": keyword, 
                "type": "Top"
            }
            if cursor:
                params["cursor"] = cursor
                
            try:
                response = requests.get(self.url, headers=headers, params=params, timeout=15)
                if response.status_code != 200:
                    print(f"Twitter API Error: {response.status_code} - {response.text}", flush=True)
                    break
                    
                data = response.json()
                page_tweets = []
                
                # New structure parsing based on user's JSON example
                raw_data = data.get('data', [])
                for item in raw_data:
                    # Map the new structure to our expected internal format
                    author_data = item.get('author', {})
                    page_tweets.append({
                        'text': item.get('text'),
                        'author': author_data.get('name', 'Twitter User'),
                        'platform': 'Twitter',
                        'published_date': item.get('createdAt')
                    })
                
                if not page_tweets:
                    print(f"DEBUG: No more tweets found, stopping at {len(all_tweets)}", flush=True)
                    break
                    
                all_tweets.extend(page_tweets)
                print(f"DEBUG: Fetched {len(all_tweets)} tweets so far", flush=True)
                
                # Pagination using pagination.nextCursor from response
                new_cursor = data.get('pagination', {}).get('nextCursor')
                if not new_cursor or new_cursor == cursor:
                    break
                cursor = new_cursor
                
                if len(page_tweets) < 2: # More relaxed threshold
                    break
                    
            except Exception as e:
                print(f"Twitter Scraper Exception: {e}", flush=True)
                break
                
        return {'tweets': all_tweets[:limit]}