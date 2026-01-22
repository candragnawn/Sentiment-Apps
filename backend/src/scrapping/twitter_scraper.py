import requests

class TwitterScraper:
    def __init__(self):
        self.api_key = "47773023ccmsh4d989cd732e0acbp196299jsnf948acca4a2c"
        self.url = "https://twitter135.p.rapidapi.com/Search" 
        self.host = "twitter135.p.rapidapi.com"

    def fetch_tweets(self, keyword, limit=100):
        print(f"twitter: mencari tweet via RapidAPI untuk: '{keyword}'...")
        
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        
        querystring = {"q": keyword, "count": str(limit)}

        try:
            response = requests.get(self.url, headers=headers, params=querystring)
            response.raise_for_status()
            json_data = response.json()

            all_tweets = []
            
            try:
                if 'data' in json_data:
                    search_data = json_data['data'].get('search_by_raw_query', {})
                    timeline = search_data.get('search_timeline', {}).get('timeline', {})
                    instructions = timeline.get('instructions', [])
                    
                    for instr in instructions:
                        if instr.get('type') == 'TimelineAddEntries':
                            for entry in instr.get('entries', []):
                                if 'tweet_results' in str(entry):
                                    try:
                                        tweet_data = entry['content']['itemContent']['tweet_results']['result']
                                        all_tweets.append(tweet_data)
                                    except:
                                        continue
            except Exception:
                all_tweets = json_data.get('data', [])

            if not all_tweets and json_data:
                all_tweets = [json_data] if isinstance(json_data, dict) else json_data

            print(f"success pull {len(all_tweets)} data from tweet")
            return {'tweets': all_tweets}
            
        except Exception as e:
            print(f"rapid error: {e}")
            return {'tweets': []}