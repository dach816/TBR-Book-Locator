import integrations
import os

def test_everand_query(requests_mock):
    isbn = "0062802402"
    requests_mock.get(f"{integrations.everand_query_url}?query={isbn}", json={"results":{"audiobooks":{"content":{"documents":[{"book_preview_url":"url"}]}}}, "total_results_count": 1})
    bookInfo = integrations.query_everand(isbn)
    assert bookInfo.hasAudiobook == True
    assert bookInfo.hasEbook == False
    assert bookInfo.audiobookLinks == ["url"]
    assert len(bookInfo.ebookLinks) == 0

def test_everand_data_audiobook():
    # 1 audiobook link
    json = {"results":{"audiobooks":{"content":{"documents":[{"book_preview_url":"url"}]}}}, "total_results_count": 1}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo.hasAudiobook == True
    assert bookInfo.hasEbook == False
    assert bookInfo.audiobookLinks == ["url"]
    assert len(bookInfo.ebookLinks) == 0

    # 0 audiobook links
    json = {"results":{"audiobooks":{"content":{"documents":[]}}}, "total_results_count": 1}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo.hasAudiobook == False
    assert bookInfo.hasEbook == False
    assert len(bookInfo.audiobookLinks) == 0
    assert len(bookInfo.ebookLinks) == 0

    # 2 audiobook links
    json = {"results":{"audiobooks":{"content":{"documents":[{"book_preview_url":"url1"}, {"book_preview_url":"url2"}]}}}, "total_results_count": 1}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo.hasAudiobook == True
    assert bookInfo.hasEbook == False
    assert bookInfo.audiobookLinks == ["url1", "url2"]
    assert len(bookInfo.ebookLinks) == 0

def test_everand_data_ebook():
    # 1 ebook link
    json = {"results":{"books":{"content":{"documents":[{"book_preview_url":"url"}]}}}, "total_results_count": 1}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo.hasAudiobook == False
    assert bookInfo.hasEbook == True
    assert len(bookInfo.audiobookLinks) == 0
    assert bookInfo.ebookLinks == ["url"]

    # 0 ebook links
    json = {"results":{"books":{"content":{"documents":[]}}}, "total_results_count": 1}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo.hasAudiobook == False
    assert bookInfo.hasEbook == False
    assert len(bookInfo.audiobookLinks) == 0
    assert len(bookInfo.ebookLinks) == 0

    # 2 ebook links
    json = {"results":{"books":{"content":{"documents":[{"book_preview_url":"url1"}, {"book_preview_url":"url2"}]}}}, "total_results_count": 1}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo.hasAudiobook == False
    assert bookInfo.hasEbook == True
    assert len(bookInfo.audiobookLinks) == 0
    assert bookInfo.ebookLinks == ["url1", "url2"]

def test_everand_data_none():
    json = {"results":{}, "total_results_count": 0}
    bookInfo = integrations.handle_everand_data(json)
    assert bookInfo == None

def test_everand_links_not_found():
    # Empty results
    links = integrations.get_everand_book_links({}, "test")
    assert len(links) == 0

    # Book type not in json
    json = {"audiobooks":{"content":{"documents":[{"book_preview_url":"url"}]}}}
    links = integrations.get_everand_book_links(json, "test")
    assert len(links) == 0

    # content not in json
    json = {"audiobooks":{"test":{}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert len(links) == 0

    # documents not in json
    json = {"audiobooks":{"content":{"test":[]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert len(links) == 0

    # Book url not in json
    json = {"audiobooks":{"content":{"documents":[{"test":"url"}]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert len(links) == 0

    # Empty documents
    json = {"audiobooks":{"content":{"documents":[]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert len(links) == 0

    # Book url is null
    json = {"audiobooks":{"content":{"documents":[{"test":None}]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert len(links) == 0

def test_everand_links_found():
    json = {"audiobooks":{"content":{"documents":[{"book_preview_url":"url"}]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert links == ["url"]
    
    json = {"audiobooks":{"content":{"documents":[{"book_preview_url":"url1"}, {"book_preview_url":"url2"}]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert links == ["url1", "url2"]
    
    json = {"audiobooks":{"content":{"documents":[{"book_preview_url":"url1"}, {"book_preview_url":None}]}}}
    links = integrations.get_everand_book_links(json, "audiobooks")
    assert links == ["url1"]

def test_hardcover_data():
    # Get 1 good result
    json = {"data": {"search": {"results": {"hits": [{"document": {"author_names": ["Author1, Author2"],"description": "Book description","has_audiobook": True,"has_ebook": True,"image": {"url": "image url"},"isbns": ["9781797113647","1534403019"],"pages": 496,"rating": 3.978260869565217,"release_date": "2018-01-01","slug": "hardcover-slug","title": "Book Title"}}]}}}}
    bookDetails = integrations.handle_hardcover_data(json)
    assert len(bookDetails) == 1

    book = bookDetails[0]
    assert book.authors == "Author1, Author2"
    assert book.coverImageUrl == "image url"
    assert book.description == "Book description"
    assert book.isbns == ["9781797113647","1534403019"]
    assert book.pages == 496
    assert book.rating == 3.978260869565217
    assert book.releaseDate == "2018-01-01"
    assert book.title == "Book Title"
    assert book.url == f"{integrations.hardcover_book_url}hardcover-slug"

    # Get 1 good result (has_ebook false)
    json = {"data": {"search": {"results": {"hits": [{"document": {"author_names": ["Author1, Author2"],"description": "Book description","has_audiobook": True,"has_ebook": False,"image": {"url": "image url"},"isbns": ["9781797113647","1534403019"],"pages": 496,"rating": 3.978260869565217,"release_date": "2018-01-01","slug": "hardcover-slug","title": "Book Title"}}]}}}}
    bookDetails = integrations.handle_hardcover_data(json)
    assert len(bookDetails) == 1

    # Get 1 good result (has_audiobook false)
    json = {"data": {"search": {"results": {"hits": [{"document": {"author_names": ["Author1, Author2"],"description": "Book description","has_audiobook": False,"has_ebook": True,"image": {"url": "image url"},"isbns": ["9781797113647","1534403019"],"pages": 496,"rating": 3.978260869565217,"release_date": "2018-01-01","slug": "hardcover-slug","title": "Book Title"}}]}}}}
    bookDetails = integrations.handle_hardcover_data(json)
    assert len(bookDetails) == 1

    # Get 1 bad result
    json = {"data": {"search": {"results": {"hits": [{"document": {"author_names": ["Author1, Author2"],"description": "Book description","has_audiobook": False,"has_ebook": False,"image": {"url": "image url"},"isbns": ["9781797113647","1534403019"],"pages": 496,"rating": 3.978260869565217,"release_date": "2018-01-01","slug": "hardcover-slug","title": "Book Title"}}]}}}}
    bookDetails = integrations.handle_hardcover_data(json)
    assert len(bookDetails) == 0

    # Get no results
    json = {"data": {"search": {"results": {"hits": []}}}}
    bookDetails = integrations.handle_hardcover_data(json)
    assert len(bookDetails) == 0
