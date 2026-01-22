import yt_dlp

class YoutubeScraper:
    def search_and_fetch(self, keyword, max_videos = 20):
        print(f"Mencari video YouTube untuk: {keyword}")
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True, 
            'force_generic_extractor': True,
        }
        
        video_results = []
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
                search_query = f"ytsearch{max_videos}:{keyword}"
                info = ydl.extract_info(search_query, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        video_results.append({
                            'platform': 'YouTube',
                            'author': entry.get('uploader', 'Unknown'),
                            'text': entry.get('title', ''),
                            'url': entry.get('url', '')
                        })
            
            print(f" Berhasil mengambil {len(video_results)} video.")
            return video_results
            
        except Exception as e:
            print(f" Error yt-dlp: {e}")
            return []