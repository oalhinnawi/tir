import React from 'react';
import Content_bar from './Content_bar.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Jumbotron, Card, Container, Row, Col } from 'react-bootstrap';
import './Home.css';
import reddit from './reddit.PNG';
import raw_text from './raw_text.png';
import results from './results.png';

class Home extends React.Component{

    render(){
        return(
            //Import the Navbar
        <React.Fragment>
            <Content_bar className = 'Content_bar' />
            <div>
              <Jumbotron><h1>What is Tir?</h1></Jumbotron>
              <p className = 'intro'>
                  <b>Tir</b> is a machine-learning architecture used for an enhanced form of Topic Modeling. <b>Tir</b> aims to provide a topic analysis,
                  sentiment analysis and latent context to the documents or texts that it scans. <b>Tir</b> will then return an in-depth and accurate summation 
                  of the relevant pieces above. 
              </p>

                <container>

                    <Col>
                    <div class="row mt-7"></div>
                     <Row className="justify-content-md-center"> {/*First row of the card-show */}
                <div className = 'Card1' class = {Card}>
                    <Card style={{ width: '35rem'}}>
                        <Card.Header>Sample Reddit Posts to be analyzed</Card.Header>
                        <Card.Img src={reddit} />
                    </Card>
                </div>
                </Row>

                <div class="row mt-4"></div>

                <Row className="mt-7 justify-content-center"> {/*Second row of the card-show */}
                <div className = 'Card2' class = {Card}>
                    <Card style={{ width: '35rem'}}>
                        <Card.Header>Scraped Reddit data ready to be processed</Card.Header>
                        <Card.Img src={raw_text} />
                    </Card>
                </div>
                </Row> 

                <div class="row mt-4"></div>

                <Row className="justify-content-md-center"> {/*Third row of the card-show */}
                <div className = 'Card3' class = {Card}>
                    <Card style={{ width: '15rem'}}>
                        <Card.Header>Results after analysis</Card.Header>
                        <Card.Img src={results} />
                    </Card>
                </div>
                </Row>

                <div class="row mt-4"></div>

                <Row className="justify-content-md-center"> {/* Ending Description */} 
                <p className = 'ending'>
                  Now that you have an idea of how it works, go test it out on the <a href = '/Topic_modeling'> Topic Modeling </a> page!
              </p>
                
                </Row>

                </Col>
                </container>

            </div>
        </React.Fragment>

        //Build the rest of the homepage
        

        )
    }
}
export default Home;