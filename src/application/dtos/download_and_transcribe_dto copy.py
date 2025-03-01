from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class FetchAndTranscribeDTO:
    url: str
    language: str
    status: str
    userId: str
    trasncriberType: str


    def to_dict(self) -> dict:
        return asdict(self)

