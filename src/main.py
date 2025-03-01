import uvicorn
import asyncio
import json
import aio_pika

from infrastructure.rabbitmq import RabbitMQ
from infrastructure.youtube_dowloader import YoutubeDownloader
from infrastructure.whisper import WhisperTranscriber



from application.use_cases.transcriber import TranscribeUseCase
from application.use_cases.downloader import DownloadAudioUseCase
from application.dtos.download_and_transcribe_dto import FetchAndTranscribeDTO
from application.use_cases.fetch_and_transcribe import FetchAndTranscribeUseCase

rabbitmq = RabbitMQ()


youtubeDownloader = YoutubeDownloader()
whisperTranscriber = WhisperTranscriber()
transcribe = TranscribeUseCase(whisperTranscriber)
download = DownloadAudioUseCase(youtubeDownloader)

fetch_transcriber = FetchAndTranscribeUseCase(download, transcribe, rabbitmq)

async def process_transcription(message: aio_pika.IncomingMessage):
    async with message.process():  # Confirma o processamento automaticamente
        raw_body = message.body  # Bytes
        
        body_str = raw_body.decode()  # Converte para string
        data = json.loads(body_str)  # Converte JSON para dicionário
        dataObj = FetchAndTranscribeDTO(
            language=data.get("language"),
            status=data.get("status"),
            url=data.get("url"),
            trasncriberType=data.get("trasncriberType"),
            userId=data.get("userId")
        )

        await fetch_transcriber.execute(dataObj)

async def main():

    try:
        RabbitMQ.set_url("amqp://guest:guest@localhost:5672")
        rabbitmq = RabbitMQ()
        await rabbitmq.connection()
        await rabbitmq.create_channel()
        await rabbitmq.subscribe("ddd", process_transcription)
        await asyncio.Future()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())