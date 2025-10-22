import requests
from book_info import BookLinks, BookDetails, BookLink

everand_query_url = "https://www.everand.com/search/query"

def query_everand_isbns(isbns: list[str]) -> BookLinks:
    results = map(query_everand, isbns)
    filteredResults = filter(lambda r: r is not None, results)
    bookLinks = BookLinks([], [])
    for result in filteredResults:
        bookLinks.audiobookLinks.extend(result.audiobookLinks)
        bookLinks.ebookLinks.extend(result.ebookLinks)
    

    bookLinks.audiobookLinks = unique_list_by_id(bookLinks.audiobookLinks)
    bookLinks.ebookLinks = unique_list_by_id(bookLinks.ebookLinks)
    return bookLinks

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
    ebookLinks = get_everand_book_links(results, "books")
    return BookLinks(audiobookLinks, ebookLinks)

def get_everand_book_links(results, bookType: str) -> list[BookLink]:
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
        if not ("id" in b and b["id"]):
            continue

        if not ("book_preview_url" in b and b["book_preview_url"]):
            continue

        bookLink = BookLink(b["id"], None, None, b["book_preview_url"])
        if "image_url" in b and b["image_url"]:
            bookLink.coverImageUrl = b["image_url"]

        if "title" in b and b["title"]:
            bookLink.title = b["title"]

        links.append(bookLink)

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
        coverImageUrl = document["image"]["url"] if "image" in document and "url" in document["image"] else None
        isbns = document["isbns"] if "isbns" in document else None
        rating = document["rating"] if "rating" in document else None
        description = document["description"] if "description" in document else None
        releaseDate = document["release_date"] if "release_date" in document else None
        url = f"{hardcover_book_url}{document["slug"]}" if "slug" in document else None
        pages = document["pages"] if "pages" in document else None
        id = document["id"] if "id" in document else None
        bookDetails = BookDetails(title, authors, coverImageUrl, isbns, rating, description, releaseDate, url, pages, id)
        results.append(bookDetails)

    print(results)
    return results

def unique_list_by_id(list):
    if not list:
        return list

    seen = set()
    uniqueList = []
    for x in list:
        key = x.id
        if key not in seen:
            seen.add(key)
            uniqueList.append(x)

    return uniqueList