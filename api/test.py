import integrations

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