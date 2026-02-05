import requests

class TwitterScraper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://twitter135.p.rapidapi.com/Search" 
        self.host = "twitter135.p.rapidapi.com"

    def fetch_tweets(self, keyword, limit=500):
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        params = {"q": keyword, "count": str(limit)}

        try:
            response = requests.get(self.url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            tweets = []
            
            try:
                if 'data' in data:
                    timeline = data['data'].get('search_by_raw_query', {}).get('search_timeline', {}).get('timeline', {})
                    for instr in timeline.get('instructions', []):
                        if instr.get('type') == 'TimelineAddEntries':
                            for entry in instr.get('entries', []):
                                if 'tweet_results' in str(entry):
                                    try:
                                        tweets.append(instr['entries'][0]['content']['itemContent']['tweet_results']['result']) if 'tweet_results' in str(entry) else None
                                        # Simple fallback/direct access if structure is nested
                                        tweets.append(entry['content']['itemContent']['tweet_results']['result'])
                                    except: continue
            except:
                tweets = data.get('data', [])

            if not tweets and data:
                tweets = [data] if isinstance(data, dict) else data

            return {'tweets': tweets}
        except Exception:
            return {'tweets': []}