import whisper
from config.settings import settings
from infrastructure.interfaces.transcriber import Transcriber

class WhisperTranscriber(Transcriber):
    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL)

    def transcribe(self, audio_path: str) -> str:
        try:
            
            result = self.model.transcribe(audio_path, verbose=True)
        
            return result["text"]
        except Exception as e:
            print(e)