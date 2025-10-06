import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Search from './components/Search';
import { Container, Row, Navbar, Nav, NavDropdown } from 'react-bootstrap';

function App() {
  return (
    <div data-bs-theme="dark">
      <Navbar className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="#home">TBR Book Locator</Navbar.Brand>
        </Container>
      </Navbar>
      <Container id='search-page'>
        <Row>
          <h1 className='mb-5 mt-3' style={{ textAlign: 'center', color: 'lightgray' }}>Book Locator</h1>
        </Row>
        <Search />
      </Container>
    </div>
  )
}

export default App
