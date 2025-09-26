import requests
from book_info import BookInfo

everand_query_url = "https://www.everand.com/search/query"

def query_everand(query: str) -> BookInfo:
    response = requests.get(everand_query_url, params={"query": query})
    response.raise_for_status()

    data = response.json()
    return handle_everand_data(data)

def handle_everand_data(data) -> BookInfo:
    resultCount = data["total_results_count"]
    if resultCount == 0:
        return None

    results = data["results"]
    audiobookLinks = get_everand_book_links(results, "audiobooks")
    hasAudiobook = len(audiobookLinks) > 0

    ebookLinks = get_everand_book_links(results, "books")
    hasEbook = len(ebookLinks) > 0
    return BookInfo(hasAudiobook, hasEbook, audiobookLinks, ebookLinks)

def get_everand_book_links(results, bookType: str) -> list[str]:
    if bookType not in results:
        return []

    bookResults = results[bookType]
    if "content" not in bookResults:
        return []
    
    content = bookResults["content"]
    if "documents" not in content:
        return []

    books = content["documents"]
    if not books:
        return []

    links = []
    for b in books:
        if "book_preview_url" in b and b["book_preview_url"]:
            links.append(b["book_preview_url"])

    return links