import requests
from book_info import BookLinks, BookDetails

everand_query_url = "https://www.everand.com/search/query"

def query_everand(query: str) -> BookLinks:
    response = requests.get(everand_query_url, params={"query": query})
    response.raise_for_status()

    data = response.json()
    return handle_everand_data(data)

def handle_everand_data(data) -> BookLinks:
    resultCount = data["total_results_count"]
    if resultCount == 0:
        return None

    results = data["results"]
    audiobookLinks = get_everand_book_links(results, "audiobooks")
    hasAudiobook = len(audiobookLinks) > 0

    ebookLinks = get_everand_book_links(results, "books")
    hasEbook = len(ebookLinks) > 0
    return BookLinks(hasAudiobook, hasEbook, audiobookLinks, ebookLinks)

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

hardcover_api_url = "https://api.hardcover.app/v1/graphql"
hardcover_book_url = "https://hardcover.app/books/"

def search_hardcover(query: str, token: str) -> list[BookDetails]:
    body = """
        query SearchQuery($queryText: String!) {
            search(query: $queryText) {
            error
            page
            per_page
            query
            query_type
            results
            }
        }"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Authorization": token
    }
    response = requests.post(hardcover_api_url, json={"query": body, "variables": {"queryText": query}}, headers=headers)
    response.raise_for_status()

    data = response.json()
    return handle_hardcover_data(data)

def handle_hardcover_data(data) -> list[BookDetails]:
    searchResults = data["data"]["search"]["results"]["hits"]
    results = []
    for searchResult in searchResults:
        document = searchResult["document"]
        if not document["has_audiobook"] and not document["has_ebook"]:
            continue

        title = document["title"] if "title" in document else None
        authors = ", ".join(document["author_names"]) if "author_names" in document else None
        coverImageUrl = document["image"]["url"] if "image" in document else None
        isbns = document["isbns"] if "isbns" in document else None
        rating = document["rating"] if "rating" in document else None
        description = document["description"] if "description" in document else None
        releaseDate = document["release_date"] if "release_date" in document else None
        url = f"{hardcover_book_url}{document["slug"]}" if "slug" in document else None
        pages = document["pages"] if "pages" in document else None
        bookDetails = BookDetails(title, authors, coverImageUrl, isbns, rating, description, releaseDate, url, pages)
        results.append(bookDetails)

    print(results)
    return results