import yt_dlp
from config.settings import settings 

class YoutubeDownloader:
    def download_audio(self, url: str) -> str:
        output_path = f"{settings.TEMP_DIR}/{url.split('=')[-1]}.mp3"
        print("output_path", output_path)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'verbose': True,  # Enable detailed output for debugging
            
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path