from ntscraper import Nitter

class TwitterScraper:
    def __init__(self):
        self.nitter = Nitter()

    def fetch_tweets(self, keyword, limit=50):
        print(f"twitter: mencari tweet tentang: '{keyword}'...")
        try:
            tweets = self.nitter.get_tweets(keyword, mode='term', number=limit)
            return tweets
        except Exception as e:
            return {'tweets':[]}
            