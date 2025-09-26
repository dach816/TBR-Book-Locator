from dataclasses import dataclass

@dataclass
class BookInfo:
    hasAudiobook: bool
    hasEbook: bool
    audiobookLinks: list[str]
    ebookLinks: list[str]