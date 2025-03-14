from openai import AsyncOpenAI
from config.settings import settings
from infrastructure.interfaces.transcriber import Transcriber


class WhisperTranscribeClient(Transcriber):
    def __init__(self, api_key):
        self.model = "whisper-1"
        self.openAi = AsyncOpenAI(api_key=api_key)

    async def transcribe(self, audio_path: str) -> str:
        print("entrei", audio_path)
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = await self.openAi.audio.transcriptions.create(
                    model=self.model, file=audio_file, language="en"
                )
            return transcript.text
        except Exception as e:
            print(e)
            raise
