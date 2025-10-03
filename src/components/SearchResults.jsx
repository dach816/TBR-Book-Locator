import { Row } from "react-bootstrap";
import SearchResult from "./SearchResult"

function SearchResults(props) {
    return (
        <>
            <Row style={{ justifyContent: 'center' }} className="mt-5">
                {props.resultList.map((item) => (
                    <SearchResult key={item.id} item={item} />
                ))}
            </Row>
        </>  
    );
}

export default SearchResults;