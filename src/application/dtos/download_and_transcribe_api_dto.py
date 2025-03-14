from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class FetchAndTranscribeApiDTO:
    url: str
    language: str

    def to_dict(self) -> dict:
        return asdict(self)
