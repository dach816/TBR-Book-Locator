import requests
from book_info import BookInfo

everand_query_url = "https://www.everand.com/search/query"

def query_everand(query: str) -> BookInfo:
    response = requests.get(everand_query_url, params={"query": query})
    response.raise_for_status()

    data = response.json()
    resultCount = data['total_results_count']
    if resultCount == 0:
        return None

    results = data['results']
    hasAudiobook = "audiobooks" in results
    hasEbook = "books" in results
    bookInfo = BookInfo(hasAudiobook, hasEbook)
    return bookInfo