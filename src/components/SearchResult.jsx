import { Card, Col } from "react-bootstrap";

function SearchResult(props) {
    return (
        <Col xs={12} md={4}>
            <Card>
                <Card.Img variant="top" src={props.item.coverImageUrl} height={250} width={150}/>
                <Card.Body>
                    <Card.Text>{props.item.rating.toFixed(2)}/5⭐</Card.Text>
                    <Card.Title>{props.item.title}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">{props.item.authors}</Card.Subtitle>
                    <Card.Text>{props.item.description}</Card.Text>
                    <Card.Link href={props.item.url}>See in Hardcover</Card.Link>
                </Card.Body>
            </Card>
        </Col>
    );
}

export default SearchResult;