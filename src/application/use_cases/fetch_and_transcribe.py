import json
from .downloader import DownloadAudioUseCase
from .transcriber import TranscribeUseCase
from ..dtos.download_and_transcribe_dto import FetchAndTranscribeDTO
from infrastructure.interfaces.message_broker import MessageBroker


class FetchAndTranscribeUseCase:

    def __init__(
        self,
        downloadAudioUseCase: DownloadAudioUseCase,
        transcribeUseCase: TranscribeUseCase,
        broker: MessageBroker,
    ):
        self.downloadAudioUseCase = downloadAudioUseCase
        self.transcribeUseCase = transcribeUseCase
        self.rabbitmq = broker

    async def execute(self, data: FetchAndTranscribeDTO):

        output = await self.downloadAudioUseCase.execute(data.url)
        transcription = await self.transcribeUseCase.execute(output.path)

        # print("transcription transcription transcription", transcription)
        data = data.to_dict()
        data["text"] = transcription.text
        data["status"] = "completed"

        print("data data", data)
        print(transcription.to_dict())
        dataJson = json.dumps(transcription.to_dict())

        await self.rabbitmq.publish("transcription-queue", data)
