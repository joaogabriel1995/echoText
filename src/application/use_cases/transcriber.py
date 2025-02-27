from infrastructure.interfaces.downloader import  Downloader
from infrastructure.interfaces.transcriber import Transcriber
from infrastructure.interfaces.message_broker import MessageBroker
from domain.transcription import Transcription

class TranscribeUseCase:
    def __init__(self, downloader: Downloader, transcriber: Transcriber, broker: MessageBroker):
        self.downloader = downloader
        self.transcriber = transcriber
        self.broker = broker

    async def execute(self, url: str) -> Transcription:
        """Interface principal, publica a URL na fila."""
        # await self.publish_url(url)
        print("Cheguei at[e aqui]", url)

        output_path = self.downloader.download_audio(url)
        text = self.transcriber.transcribe(output_path)

        print(text)

        return Transcription(text=text, url=url)