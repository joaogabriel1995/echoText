import os


class Settings:
    TEMP_DIR = "temp_audio"
    WHISPER_MODEL = "small"  # Opções: tiny, base, small, medium, large


settings = Settings()

if not os.path.exists(settings.TEMP_DIR):
    os.makedirs(settings.TEMP_DIR)
