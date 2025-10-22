import {useState} from 'react'
import { Card, Col, Row, Button } from "react-bootstrap";
import TruncatedText from "./TruncatedText";
import BookAvailability from './BookAvailability';
import Loading from './Loading';

function SearchResult(props) {
    const [resultsJson, setResultsJson] = useState(null)
    const [loading, setLoading] = useState(false)

    const onSearch = (isbns) => {
        if (!isbns) {
            return
        }

        // Add error handling
        setLoading(true)
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ isbns: isbns })
        };
        fetch("/api/query/everand", requestOptions)
            .then(res => res.json())
            .then(data => {
                console.log(data)
                setLoading(false)
                setResultsJson(data)
            })
    };

    return (
        <Col xs={12}>
            <Card className="mb-2">
                <Card.Body>
                    <Row>
                        <Col xs={3} md={2} lg={1}>
                            <Card.Img src={props.item.coverImageUrl} className="mb-2" alt={`Cover art for ${props.item.title}.`}/>
                        </Col>
                        <Col>
                            <Card.Title>{props.item.title}</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">{props.item.authors}</Card.Subtitle>
                            <Card.Text>
                                {props.item.releaseDate ? new Date(props.item.releaseDate).getFullYear() : "?"}
                                <i className="bi bi-dot"></i>
                                {props.item.rating ? props.item.rating.toFixed(2) : "?"}⭐
                                <i className="bi bi-dot"></i>
                                {props.item.pages ? props.item.pages.toLocaleString('en-US') : "?"} pages
                            </Card.Text>
                        </Col>
                    </Row>
                    <Card.Text>
                        <TruncatedText fullText={props.item.description} truncatedText={props.item.description ? props.item.description.substring(0, 150) : ''}/>
                    </Card.Text>
                </Card.Body>
                <Card.Footer style={{ textAlign: 'center' }}>
                    <Button variant='primary' href={props.item.url} className='mx-1 mt-1'>Go to book in Hardcover <i className="bi bi-box-arrow-up-right"/></Button>
                    <Button variant='primary' onClick={() => onSearch(props.item.isbns)} className='mx-1 mt-1'>Search Everand</Button>
                    {loading ? <Loading /> : resultsJson && <BookAvailability result={resultsJson} parentId={props.item.id}/>}
                </Card.Footer>
            </Card>
        </Col>
    );
}

export default SearchResult;