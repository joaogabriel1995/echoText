from abc import ABC, abstractmethod

class Downloader(ABC):
    @abstractmethod
    def download_audio(self, url: str) -> str:
        pass