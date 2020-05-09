import React from 'react';
import {Navbar, Nav,} from 'react-bootstrap';

export default class Content_bar extends React.Component{

  render(){
    return(
        <>
        <Navbar bg="dark" variant="dark">
          <Nav className="mr-auto">
            <Nav.Link href = '/'> Project Tir </Nav.Link>
            <Nav.Link href = '/Topic_modeling'> Topic Modeling </Nav.Link>
            <Nav.Link href = '/Faq'> F.A.Q </Nav.Link>
          </Nav>
        </Navbar>
        </>
      )
    }
}