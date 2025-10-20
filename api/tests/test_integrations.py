import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import integrations

class Test_Everand:
    def setup_method(self):
        AUDIOBOOK = "audiobooks"
        EBOOK = "books"
        bookLink = {"book_preview_url":"url"}
        noneBookLink = {"book_preview_url":None}

        generateBooksByLinks = lambda bookType, links: {bookType:{"content":{"documents":links}}}
        generateBooks = lambda bookType, numLinks: generateBooksByLinks(bookType, [bookLink] * numLinks)
        generateResults = lambda bookType, numLinks: {"results":generateBooks(bookType, numLinks), "total_results_count":1}

        self.audiobookResultsNoLinks = generateResults(AUDIOBOOK, 0)
        self.audiobookResultsOneLink = generateResults(AUDIOBOOK, 1)
        self.audiobookResultsTwoLinks = generateResults(AUDIOBOOK, 2)
        self.ebookResultsNoLinks = generateResults(EBOOK, 0)
        self.ebookResultsOneLink = generateResults(EBOOK, 1)
        self.ebookResultsTwoLinks = generateResults(EBOOK, 2)

        self.audiobookNoLinks = generateBooks(AUDIOBOOK, 0)
        self.audiobookOneLink = generateBooks(AUDIOBOOK, 1)
        self.audiobookTwoLinks = generateBooks(AUDIOBOOK, 2)
        self.audiobookTwoLinksOneNone = generateBooksByLinks(AUDIOBOOK, [bookLink, noneBookLink])

        self.noResults = {"results":{}, "total_results_count": 0}
        self.noAudiobookContent = {AUDIOBOOK:{}}
        self.noAudiobookDocuments = {AUDIOBOOK:{"content":{}}}
        self.audiobookLinksNone = generateBooksByLinks(AUDIOBOOK, [noneBookLink])

    def test_everand_query(self, requests_mock):
        isbn = "0062802402"
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn}", json=self.audiobookResultsOneLink)
        bookInfo = integrations.query_everand(isbn)
        assert bookInfo.hasAudiobook == True
        assert bookInfo.hasEbook == False
        assert bookInfo.audiobookLinks == ["url"]
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_query_isbns_one_audiobook_one_ebook(self, requests_mock):
        isbn1 = "9781980080633"
        isbn2 = "9781250765383"
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn1}", json=self.audiobookResultsOneLink)
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn2}", json=self.ebookResultsOneLink)
        bookInfo = integrations.query_everand_isbns([isbn1, isbn2])
        assert bookInfo.hasAudiobook == True
        assert bookInfo.hasEbook == True
        assert bookInfo.audiobookLinks == ["url"]
        assert bookInfo.ebookLinks == ["url"]

    def test_everand_query_isbns_no_audiobook_one_ebook(self, requests_mock):
        isbn1 = "6258327583"
        isbn2 = "9781250765383"
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn1}", json=self.noResults)
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn2}", json=self.ebookResultsOneLink)
        bookInfo = integrations.query_everand_isbns([isbn1, isbn2])
        assert bookInfo.hasAudiobook == False
        assert bookInfo.hasEbook == True
        assert len(bookInfo.audiobookLinks) == 0
        assert bookInfo.ebookLinks == ["url"]

    def test_everand_query_isbns_no_audiobook_two_ebook(self, requests_mock):
        isbn1 = "9781250880796"
        isbn2 = "9781250765383"
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn1}", json=self.ebookResultsOneLink)
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn2}", json=self.ebookResultsOneLink)
        bookInfo = integrations.query_everand_isbns([isbn1, isbn2])
        assert bookInfo.hasAudiobook == False
        assert bookInfo.hasEbook == True
        assert len(bookInfo.audiobookLinks) == 0
        assert bookInfo.ebookLinks == ["url"]

    def test_everand_query_isbns_one_audiobook_no_ebook(self, requests_mock):
        isbn1 = "9781980080633"
        isbn2 = "6258327583"
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn1}", json=self.audiobookResultsOneLink)
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn2}", json=self.noResults)
        bookInfo = integrations.query_everand_isbns([isbn1, isbn2])
        assert bookInfo.hasAudiobook == True
        assert bookInfo.hasEbook == False
        assert bookInfo.audiobookLinks == ["url"]
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_query_isbns_two_audiobook_no_ebook(self, requests_mock):
        isbn1 = "9781980080633"
        isbn2 = "1980080631"
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn1}", json=self.audiobookResultsOneLink)
        requests_mock.get(f"{integrations.everand_query_url}?query={isbn2}", json=self.audiobookResultsOneLink)
        bookInfo = integrations.query_everand_isbns([isbn1, isbn2])
        assert bookInfo.hasAudiobook == True
        assert bookInfo.hasEbook == False
        assert bookInfo.audiobookLinks == ["url"]
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_data_audiobook_one_link(self):
        bookInfo = integrations.handle_everand_data(self.audiobookResultsOneLink)
        assert bookInfo.hasAudiobook == True
        assert bookInfo.hasEbook == False
        assert bookInfo.audiobookLinks == ["url"]
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_data_audiobook_no_links(self):
        bookInfo = integrations.handle_everand_data(self.audiobookResultsNoLinks)
        assert bookInfo.hasAudiobook == False
        assert bookInfo.hasEbook == False
        assert len(bookInfo.audiobookLinks) == 0
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_data_audiobook_two_links(self):
        bookInfo = integrations.handle_everand_data(self.audiobookResultsTwoLinks)
        assert bookInfo.hasAudiobook == True
        assert bookInfo.hasEbook == False
        assert bookInfo.audiobookLinks == ["url", "url"]
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_data_ebook_one_link(self):
        bookInfo = integrations.handle_everand_data(self.ebookResultsOneLink)
        assert bookInfo.hasAudiobook == False
        assert bookInfo.hasEbook == True
        assert len(bookInfo.audiobookLinks) == 0
        assert bookInfo.ebookLinks == ["url"]

    def test_everand_data_ebook_no_links(self):
        bookInfo = integrations.handle_everand_data(self.ebookResultsNoLinks)
        assert bookInfo.hasAudiobook == False
        assert bookInfo.hasEbook == False
        assert len(bookInfo.audiobookLinks) == 0
        assert len(bookInfo.ebookLinks) == 0

    def test_everand_data_ebook_two_links(self):
        bookInfo = integrations.handle_everand_data(self.ebookResultsTwoLinks)
        assert bookInfo.hasAudiobook == False
        assert bookInfo.hasEbook == True
        assert len(bookInfo.audiobookLinks) == 0
        assert bookInfo.ebookLinks == ["url", "url"]

    def test_everand_data_none(self):
        bookInfo = integrations.handle_everand_data(self.noResults)
        assert bookInfo == None

    def test_everand_links_not_found_no_results(self):
        links = integrations.get_everand_book_links({}, "test")
        assert len(links) == 0

    def test_everand_links_not_found_wrong_book_type(self):
        links = integrations.get_everand_book_links(self.audiobookOneLink, "test")
        assert len(links) == 0

    def test_everand_links_not_found_no_content(self):
        links = integrations.get_everand_book_links(self.noAudiobookContent, "audiobooks")
        assert len(links) == 0

    def test_everand_links_not_found_no_documents(self):
        links = integrations.get_everand_book_links(self.noAudiobookDocuments, "audiobooks")
        assert len(links) == 0

    def test_everand_links_not_found_no_links(self):
        links = integrations.get_everand_book_links(self.audiobookNoLinks, "audiobooks")
        assert len(links) == 0

    def test_everand_links_not_found_link_url_none(self):
        links = integrations.get_everand_book_links(self.audiobookLinksNone, "audiobooks")
        assert len(links) == 0

    def test_everand_links_found_one_link(self):
        links = integrations.get_everand_book_links(self.audiobookOneLink, "audiobooks")
        assert links == ["url"]
        
    def test_everand_links_found_two_links(self):
        links = integrations.get_everand_book_links(self.audiobookTwoLinks, "audiobooks")
        assert links == ["url", "url"]
        
    def test_everand_links_found_two_links_one_none(self):
        links = integrations.get_everand_book_links(self.audiobookTwoLinksOneNone, "audiobooks")
        assert links == ["url"]

class Test_Hardcover:
    def setup_method(self):
        generateHardcoverData = lambda hasAudiobook, hasEbook: {"data": {"search": {"results": {"hits": [{"document": {"author_names": ["Author1, Author2"],"description": "Book description","has_audiobook": hasAudiobook,"has_ebook": hasEbook,"image": {"url": "image url"},"isbns": ["9781797113647","1534403019"],"pages": 496,"rating": 3.978260869565217,"release_date": "2018-01-01","slug": "hardcover-slug","title": "Book Title", "id": "ID"}}]}}}}
        self.audiobookHardcoverData = generateHardcoverData(True, False)
        self.ebookHardcoverData = generateHardcoverData(False, True)
        self.noBookHardcoverData = generateHardcoverData(False, False)
        self.noResults = {"data": {"search": {"results": {"hits": []}}}}

    @pytest.fixture
    def book(self):
        bookDetails = integrations.handle_hardcover_data(self.audiobookHardcoverData)
        return bookDetails[0]
    
    def test_hardcover_data_book_authors(self, book):
        assert book.authors == "Author1, Author2"

    def test_hardcover_data_book_image_url(self, book):
        assert book.coverImageUrl == "image url"

    def test_hardcover_data_book_description(self, book):
        assert book.description == "Book description"

    def test_hardcover_data_book_isbns(self, book):
        assert book.isbns == ["9781797113647","1534403019"]

    def test_hardcover_data_book_pages(self, book):
        assert book.pages == 496

    def test_hardcover_data_book_rating(self, book):
        assert book.rating == 3.978260869565217

    def test_hardcover_data_book_release_date(self, book):
        assert book.releaseDate == "2018-01-01"

    def test_hardcover_data_book_title(self, book):
        assert book.title == "Book Title"

    def test_hardcover_data_hardcover_url(self, book):
        assert book.url == f"{integrations.hardcover_book_url}hardcover-slug"

    def test_hardcover_audiobook_results_size(self):
        bookDetails = integrations.handle_hardcover_data(self.audiobookHardcoverData)
        assert len(bookDetails) == 1

    def test_hardcover_ebook_results_size(self):
        bookDetails = integrations.handle_hardcover_data(self.ebookHardcoverData)
        assert len(bookDetails) == 1

    def test_hardcover_no_audiobook_no_ebook(self):
        bookDetails = integrations.handle_hardcover_data(self.noBookHardcoverData)
        assert len(bookDetails) == 0

    def test_hardcover_no_results(self):
        bookDetails = integrations.handle_hardcover_data(self.noResults)
        assert len(bookDetails) == 0
