import { useState, useEffect, useRef } from 'react'
import { Col, Row, Stack } from 'react-bootstrap';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import { useSearchParams } from 'react-router-dom';

function SearchForm({onSearch}) {
    const formRef = useRef(null);
    const [searchParams, setSearchParams] = useSearchParams();
    const queryParamSearchText = searchParams.get("query");
    const [query, setQuery] = useState(queryParamSearchText ?? '')

    function updateQuery(queryValue) {
        const next = new URLSearchParams(searchParams);
        next.set('query', queryValue);
        setSearchParams(next);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        updateQuery(query)
        onSearch(query);
    };

    useEffect(() => {
        if (queryParamSearchText) {
            formRef.current.requestSubmit();
        }
    }, [queryParamSearchText]);

    return (
        <>
            <Row style={{ justifyContent: 'center' }}>
                <Col xs={12} md={8}>
                    <Form onSubmit={handleSubmit} ref={formRef}>
                        <Stack direction="horizontal" gap={3}>
                            <Form.Control
                                className="me-auto"
                                placeholder="Search for a book title and/or author..."
                                id="queryInput" onChange={(e) => setQuery(e.target.value)}
                                value={query} />
                            <Button variant="primary" type='submit'>Search</Button>
                        </Stack>
                    </Form>
                </Col>
            </Row>
        </>
    )
}

export default SearchForm;