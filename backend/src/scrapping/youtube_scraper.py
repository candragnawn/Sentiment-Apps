import yt_dlp
from datetime import datetime

class YoutubeScraper:
    def search_and_fetch(self, keyword, max_videos=500):
        
        class MyLogger:
            def debug(self, msg): pass
            def warning(self, msg): pass
            def error(self, msg): pass

        opts = {
            'quiet': True,
            'no_warnings': True,
            'logger': MyLogger(),
            'noprogress': True,
            'extract_flat': 'in_playlist',
            'force_generic_extractor': False,
            'max_downloads': max_videos,
            'noplaylist': True,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'format': 'worst',
            'skip_download': True,
            'num_retries': 0,
            'no_color': True,
            'lazy_playlist': True,
            'cachedir': False,
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
                            except: 
                                pub_date = datetime.now().isoformat()
                        else:
                            pub_date = datetime.now().isoformat()

                        results.append({
                            'platform': 'YouTube',
                            'author': entry.get('uploader', 'Unknown'),
                            'text': entry.get('title', '') + " " + (entry.get('description', '') or ""),
                            'url': entry.get('webpage_url', entry.get('url', '')),
                            'published_date': pub_date
                        })
            return results
        except Exception as e:
            print(f"YouTube Scraper Error: {e}")
            return []