import {useState} from 'react'
import SearchForm from "./SearchForm";
import SearchResults from "./SearchResults";
import Loading from './Loading';

function Search() {
    const [resultsJson, setResultsJson] = useState(null)
    const [loading, setLoading] = useState(false)

    const onSearch = (query) => {
        if (!query) {
            return
        }

        // Add error handling
        setLoading(true)
        fetch(`/api/query/hardcover?query=${query}`).then(res => res.json()).then(data => {
            setLoading(false)
            setResultsJson(data)
        })
    };

    return (
        <>
            <SearchForm onSearch={onSearch} />
            {loading ? <Loading /> : resultsJson && <SearchResults resultList={resultsJson} />}
        </>
    )
}

export default Search;