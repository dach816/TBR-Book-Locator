import { Col, Row, Stack } from 'react-bootstrap';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'

function SearchForm({onSearch}) {
    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(e.currentTarget.elements.queryInput.value);
    };
    return (
        <>
            <Row style={{ justifyContent: 'center' }}>
                <Col xs={12} md={8}>
                    <Form onSubmit={handleSubmit}>
                        <Stack direction="horizontal" gap={3}>
                            <Form.Control className="me-auto" placeholder="Search for a book title and/or author..." id="queryInput" />
                            <Button variant="primary" type='submit'>Search</Button>
                        </Stack>
                    </Form>
                </Col>
            </Row>
        </>
    )
}

export default SearchForm;