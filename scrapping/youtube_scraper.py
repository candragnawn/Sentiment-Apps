from youtubesearchpython import VideosSearch
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT

class YouTubeScraper:
    def __init__(self):
        self.downloader = YoutubeCommentDownloader()
    def search_and_fetch(self, keyword, max_videos=4, comments_per_video=20):
        print(f"searching for videos with keyword: {keyword}")
        search = VideosSearch(keyword, limit=max_videos)
        results = search.result()['results']

        all_comments = []
        for video in results:
            video_url = video['link']
            print(f"fetching comments for video: {video['title'][:50]}...")


            try:
                comments = self.downloader.get_comments_from_url(video_url, sort_by=SORT_BY_RECENT)
                count = 0
                for comment in comments:
                    all_comments.append({'text': comment['text']})
                    count +=1
                    if count >= comments_per_video:
                        break

            except Exception as e:
                print(f"error fetching coments for video {video_url}: {e}")
        return all_comments
            


        


