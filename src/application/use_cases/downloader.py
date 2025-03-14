from infrastructure.interfaces.downloader import Downloader
from infrastructure.interfaces.transcriber import Transcriber
from infrastructure.interfaces.message_broker import MessageBroker
from domain.download import Download


class DownloadAudioUseCase:
    def __init__(self, downloader: Downloader):
        self.downloader = downloader

    async def execute(self, url: str) -> Download:

        output_path = self.downloader.download_audio(url)
        # path = f"{output_path}.mp3"

        return Download(url, output_path)
