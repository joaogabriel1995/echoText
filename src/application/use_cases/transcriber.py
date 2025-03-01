from infrastructure.interfaces.downloader import  Downloader
from infrastructure.interfaces.transcriber import Transcriber
from infrastructure.interfaces.message_broker import MessageBroker
from domain.transcription import Transcription

class TranscribeUseCase:
    def __init__(self, transcriber: Transcriber):
        self.transcriber = transcriber

    async def execute(self, audio_path: str) -> Transcription:
        """Interface principal, publica a URL na fila."""
        # await self.publish_url(url)
    
        text = self.transcriber.transcribe(f"{audio_path}.mp3")


        return Transcription(text=text, audio_path=audio_path)