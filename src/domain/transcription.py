from dataclasses import dataclass


@dataclass
class Transcription:
    text: str
    audio_path: str

    def __init__(self, text, audio_path):
        self.text = text
        self.audio_path = audio_path

    def to_dict(self):
        return {"text": self.text, "audio_path": self.audio_path}
