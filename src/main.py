import asyncio
import json
import os
from aio_pika import Message, DeliveryMode
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential


from infrastructure.rabbitmq import RabbitMQ
from infrastructure.youtube_dowloader import YoutubeDownloader
from infrastructure.whisper_client import WhisperTranscribeClient
from infrastructure.whisper import WhisperTranscriber
from application.use_cases.transcriber import TranscribeUseCase
from application.use_cases.downloader import DownloadAudioUseCase
from application.dtos.download_and_transcribe_dto import FetchAndTranscribeDTO
from application.dtos.download_and_transcribe_api_dto import FetchAndTranscribeApiDTO
from application.use_cases.fetch_and_transcribe import FetchAndTranscribeUseCase
from application.use_cases.fetch_and_transcribe_api import FetchAndTranscribeApiUseCase

load_dotenv()

# 🔹 Definir como variável global
rabbitmq = None
config = load_dotenv("../.env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
open_api_key = os.getenv("OPENAI_API_KEY")


async def initialize_rabbitmq():
    """Inicializa a conexão e o canal do RabbitMQ"""
    global rabbitmq  # Permite acesso global
    print(config)
    RabbitMQ.set_url("amqp://guest:guest@localhost:5672")
    rabbitmq = RabbitMQ()
    await rabbitmq.connection()
    await rabbitmq.create_channel()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def publish_response(
    reply_to: str, response_body: dict, correlation_id: str = None
):
    """Publica a resposta no RabbitMQ garantindo que seja um JSON válido"""
    global rabbitmq
    try:
        json_body = json.dumps(response_body, ensure_ascii=False).encode()
        message = Message(
            body=json_body,
            correlation_id=correlation_id,
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
            reply_to=reply_to,
        )

        await rabbitmq.publish(reply_to, message)

    except Exception as e:
        print(f"Erro ao publicar mensagem no RabbitMQ: {e}")
        raise


async def process_transcription_local(message):
    """Processa a transcrição de forma local"""
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            dataObj = FetchAndTranscribeDTO(
                language=data.get("language"),
                status=data.get("status"),
                url=data.get("url"),
                trasncriberType=data.get("trasncriberType"),
                userId=data.get("userId"),
            )
            await fetch_transcriber.execute(dataObj)
        except Exception as e:
            print(f"Erro no processamento local da transcrição: {str(e)}")


async def process_transcription_api(message):
    """Processa a transcrição via API e responde pelo RabbitMQ"""
    async with message.process():
        global rabbitmq
        try:
            data = json.loads(message.body.decode())
            correlation_id = message.correlation_id
            reply_to = message.reply_to
            print(f"📥 Recebeu mensagem com correlation_id: {correlation_id}")

            if not reply_to:
                print("⚠️ Erro: Mensagem sem 'reply_to', ignorando resposta RPC.")
                return

            dataObj = FetchAndTranscribeApiDTO(
                language=data.get("language"),
                url=data.get("youtube_url"),
            )
            transcript = await fetch_transcriber_api.execute(dataObj)

            await publish_response(reply_to, transcript, correlation_id)
            print(
                f"✅ Resposta enviada para {reply_to} com correlation_id {correlation_id}"
            )

        except Exception as e:
            print(f"Erro no processamento da transcrição API: {str(e)}")
            error_response = {"error": str(e)}
            try:
                await publish_response(reply_to, error_response, correlation_id)
            except Exception as err:
                print(f"Erro ao enviar erro para {reply_to}: {err}")


async def main():
    """Função principal que inicializa o serviço e as filas"""
    global rabbitmq
    try:
        await initialize_rabbitmq()

        # Inicializar dependências
        youtubeDownloader = YoutubeDownloader()
        whisperTranscriber = WhisperTranscriber()
        transcribe = TranscribeUseCase(whisperTranscriber)
        whisperTranscriberApi = WhisperTranscribeClient(open_api_key)
        transcribeApi = TranscribeUseCase(whisperTranscriberApi)
        download = DownloadAudioUseCase(youtubeDownloader)

        global fetch_transcriber, fetch_transcriber_api
        fetch_transcriber = FetchAndTranscribeUseCase(download, transcribe, rabbitmq)
        fetch_transcriber_api = FetchAndTranscribeApiUseCase(
            download, transcribeApi, rabbitmq
        )

        await rabbitmq.subscribe(
            "process_transcription_local", process_transcription_local
        )
        await rabbitmq.subscribe("process_transcription_api", process_transcription_api)

        print("✅ Serviço iniciado e ouvindo filas...")

        await asyncio.Future()

    except Exception as e:
        print(f"Erro no main: {e}")
    finally:
        await rabbitmq.close()


if __name__ == "__main__":
    asyncio.run(main())
