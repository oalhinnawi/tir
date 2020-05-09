import React from 'react';
import Content_bar from './Content_bar.js';
import { Jumbotron, Card, Container, Row, Col } from 'react-bootstrap';
import './Faq.css';


class Faq extends React.Component{

    render(){
        return(
            //Import the Navbar
        <React.Fragment>
           <div className='entire_page'>
            <Content_bar />
            <Jumbotron><h1>Project Tir</h1></Jumbotron>

            
            <container>
                <div className='faqs'>
                <dl>
                    <dt>
                   <h3>1. What is the point in all of this? </h3>
                    </dt>
                    <dd>
                    This is a test 
                    </dd>
                    <dt>
                    // Question 2 here
                    </dt>
                   <dd>
                    // Answer 2 here
                  </dd>
                    </dl>
                </div>
            </container>


          </div>  
        </React.Fragment>

        //Build the rest of the FAQ
        

        )
    }
}
export default Faq;