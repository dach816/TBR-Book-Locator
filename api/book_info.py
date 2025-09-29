from dataclasses import dataclass
import datetime
from decimal import Decimal

@dataclass
class BookLinks:
    hasAudiobook: bool
    hasEbook: bool
    audiobookLinks: list[str]
    ebookLinks: list[str]

@dataclass
class BookDetails:
    title: str
    authors: str
    coverImageUrl: str
    isbns: list[str]
    rating: Decimal
    description: str
    releaseDate: datetime
    url: str
    pages: int