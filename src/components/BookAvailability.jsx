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
        <Row className="mt-2">
            <Col className="mt-1" xs={12} sm={6}>
                <Card.Title>Audiobooks</Card.Title>
                <BookResults results={result.audiobookLinks} parentId={parentId}/>
            </Col>
            <Col className="mt-1" xs={12} sm={6}>
                <Card.Title>Ebooks</Card.Title>
                <BookResults results={result.ebookLinks} parentId={parentId}/>
            </Col>
        </Row>  
    );
}

export default BookAvailability;