import { Spinner, Row } from "react-bootstrap"

function Loading() {
    return (
        <Row style={{ justifyContent: 'center' }} role="status" className="mt-5" >
            <span className="visually-hidden">Loading...</span>
            <Spinner animation="grow" variant="danger" />
            <Spinner animation="grow" variant="warning" />
            <Spinner animation="grow" variant="success" />
            <Spinner animation="grow" variant="primary" />
            <Spinner animation="grow" variant="secondary" />
            <Spinner animation="grow" variant="dark" />
        </Row>
    )
}

export default Loading;