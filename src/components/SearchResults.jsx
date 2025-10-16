import { Card, CardBody, Row } from "react-bootstrap";
import SearchResult from "./SearchResult"

function SearchResults(props) {
    return (
        <>
            <Row style={{ justifyContent: 'center' }} className="mt-5">
                {props.resultList.length
                    ? props.resultList.map((item) => (
                        <SearchResult key={item.id} item={item} />
                    ))
                    : <Card><CardBody style={{textAlign: 'center'}}>No results</CardBody></Card>}
            </Row>
        </>  
    );
}

export default SearchResults;