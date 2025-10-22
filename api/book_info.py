from dataclasses import dataclass
import datetime
from decimal import Decimal

@dataclass
class BookLink:
    id: str
    title: str
    coverImageUrl: str
    url: str
    
@dataclass
class BookLinks:
    audiobookLinks: list[BookLink]
    ebookLinks: list[BookLink]

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
    id: str