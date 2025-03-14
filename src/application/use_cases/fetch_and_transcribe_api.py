import json
from .downloader import DownloadAudioUseCase
from .transcriber import TranscribeUseCase
from ..dtos.download_and_transcribe_api_dto import FetchAndTranscribeApiDTO
from infrastructure.interfaces.message_broker import MessageBroker


class FetchAndTranscribeApiUseCase:

    def __init__(
        self,
        downloadAudioUseCase: DownloadAudioUseCase,
        transcribeUseCase: TranscribeUseCase,
        broker: MessageBroker,
    ):
        self.downloadAudioUseCase = downloadAudioUseCase
        self.transcribeUseCase = transcribeUseCase
        self.rabbitmq = broker

    async def execute(self, data: FetchAndTranscribeApiDTO):

        output = await self.downloadAudioUseCase.execute(data.url)
        transcription = await self.transcribeUseCase.execute(output.path)

        return {"url": data.url, "language": data.language, "text": transcription.text}
