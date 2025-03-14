from abc import ABC, abstractmethod


class Transcriber(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        pass
