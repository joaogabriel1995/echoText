from dataclasses import dataclass

@dataclass
class Download:
    url: str
    path: str

    @staticmethod
    def generateName(temp_dir: str, url):
        return f"{temp_dir}/{url.split('=')[-1]}"