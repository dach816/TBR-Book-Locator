import { Card, Col, Row, Button } from "react-bootstrap";

function BookResults({results, parentId}) {
    return (
        <>
            <Row>
                {results && results.length
                    ? results.map((item) => (
                        <Button key={`${parentId}-${item.id}`} variant='link' href={item.url}>{item.title} <i className="bi bi-box-arrow-up-right"/></Button>
                    ))
                    : <p>No results</p>}
            </Row>
        </>  
    );
}

function BookAvailability({result, parentId}) {

    return (
        <>
            <Card.Title className="mt-3">Audiobooks</Card.Title>
            <BookResults results={result.audiobookLinks} parentId={parentId}/>
            <Card.Title className="mt-1">Ebooks</Card.Title>
            <BookResults results={result.ebookLinks} parentId={parentId}/>
        </>  
    );
}

export default BookAvailability;