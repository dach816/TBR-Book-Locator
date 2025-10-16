import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Search from './components/Search';
import { Container, Row, Navbar } from 'react-bootstrap';
import { BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div data-bs-theme="dark">
        <Navbar className="bg-body-tertiary" id='navbar'>
          <Container>
            <Navbar.Brand href="/">TBR Book Locator</Navbar.Brand>
          </Container>
        </Navbar>
        <Container id='search-page'>
          <Row>
            <h1 className='mb-5 mt-3' style={{ textAlign: 'center', color: 'lightgray' }}>Book Locator</h1>
          </Row>
          <Search />
        </Container>
      </div>
    </BrowserRouter>
  )
}

export default App
