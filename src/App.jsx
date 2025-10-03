import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Search from './components/Search';
import { Card, Col, Container, Row } from 'react-bootstrap';

function App() {
  return (
    <Container>
      <Row>
        <h1 className='mb-5 mt-3' style={{ textAlign: 'center' }}>Book Locator</h1>
      </Row>
      <Search />
    </Container>
  )
}

export default App
