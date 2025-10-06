import { Card, Col, Row } from "react-bootstrap";
import TruncatedText from "./TruncatedText";

function SearchResult(props) {
    return (
        <Col xs={12}>
            <Card className="mb-2">
                <Card.Body>
                    <Row>
                        <Col xs={4} md={1}>
                            <Card.Img src={props.item.coverImageUrl} className="mb-2"/>
                            <br/>
                            <Card.Link href={props.item.url}>See in Hardcover</Card.Link>
                        </Col>
                        <Col xs={8} md={11}>
                            <Card.Title>{props.item.title}</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">{props.item.authors}</Card.Subtitle>
                            <Card.Text>{props.item.rating.toFixed(2)}/5⭐</Card.Text>
                            <Card.Text>
                                <TruncatedText fullText={props.item.description} truncatedText={props.item.description ? props.item.description.substring(0, 250) : ''}/>
                            </Card.Text>
                        </Col>
                    </Row>
                </Card.Body>
            </Card>
        </Col>
    );
}

export default SearchResult;