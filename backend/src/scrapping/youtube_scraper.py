import yt_dlp
from datetime import datetime

class YoutubeScraper:
    def search_and_fetch(self, keyword, max_videos=500):
        opts = {
            'quiet': True,
            'extract_flat': True, 
            'force_generic_extractor': True,
        }
        results = []
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                query = f"ytsearch{max_videos}:{keyword}"
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        raw_date = entry.get('upload_date')
                        pub_date = None
                        if raw_date:
                            try:
                                pub_date = datetime.strptime(raw_date, '%Y%m%d').isoformat()
                            except: pass

                        results.append({
                            'platform': 'YouTube',
                            'author': entry.get('uploader', 'Unknown'),
                            'text': entry.get('title', ''),
                            'url': entry.get('url', ''),
                            'published_date': pub_date
                        })
            return results
        except Exception:
            return []