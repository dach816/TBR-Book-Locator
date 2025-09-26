import integrations

def test_everand_query_audiobook(requests_mock):
    isbn = "0062802402"
    requests_mock.get(f"{integrations.everand_query_url}?query={isbn}", json={"results":{"audiobooks":{}}, "total_results_count": 1})
    bookInfo = integrations.query_everand(isbn)
    assert bookInfo.hasAudiobook == True
    assert bookInfo.hasEbook == False

def test_everand_query_ebook(requests_mock):
    isbn = "9781534403031"
    requests_mock.get(f"{integrations.everand_query_url}?query={isbn}", json={"results":{"books":{}}, "total_results_count": 3})
    bookInfo = integrations.query_everand(isbn)
    assert bookInfo.hasAudiobook == False
    assert bookInfo.hasEbook == True

def test_everand_query_none(requests_mock):
    isbn = "9781534403032"
    requests_mock.get(f"{integrations.everand_query_url}?query={isbn}", json={"results":{}, "total_results_count": 0})
    bookInfo = integrations.query_everand(isbn)
    assert bookInfo == None