import whisper
from config.settings import settings
from infrastructure.interfaces.transcriber import Transcriber

class WhisperTranscriber(Transcriber):
    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL)

    def transcribe(self, audio_path: str) -> str:
        try:
            
            result = self.model.transcribe(audio_path)
            segmentos = []
            for segment in result.get('segments', []):
                start_time = segment.get('start', 0)
                end_time = segment.get('end', 0)
                text = segment.get('text', "")
                
                # Formata os dados do segmento e adiciona à lista
                segmentos.append(
                    f"Texto: {text}\nInício: {start_time:.2f} segundos\nFim: {end_time:.2f} segundos\n"
                )
            
            # Une todos os segmentos em uma única string
            content = "\n".join(segmentos)
            
            return content
        except Exception as e:
            print(e)