import React from 'react';
import Content_bar from './Content_bar.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Jumbotron, Row, Col, Form, Button } from 'react-bootstrap';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './Topic_modeling.css';
import axios from 'axios';


class Topic_modeling extends React.Component{

        constructor() {
          super();
          this.state = {
            subreddit: '',
            date: this.date,
            email: '',
          };
        }

        onChange = (e) => {
            this.setState({ [e.target.name]: e.target.value });
          }
    
          onSubmit = (e) => {
            e.preventDefault();
            // get our form data out of state
            const { subreddit, date, email } = this.state;
    
            axios.post('/', { subreddit, date, email })
              .then((result) => {
                //access the results here....
              });
          }

    render(){
        return(
        <React.Fragment>
            <div className='entire_page'>
            <Content_bar />
            <Jumbotron><h1>Project Tir</h1></Jumbotron>

            <container>
                <Col md={{ offset: 3 }}>   {/*First Column */}
                <Row>
                    <div className ='row1'>
                        <b><h3>Topic Modeling Settings</h3></b>
                    </div>
                </Row>


                <Form onSubmit={this.onSubmit}>
                <Form.Group controlId='model_Inputs'>

                <div className='dropdown_input'>
                    <br></br>
                <Form.Label>Select Subreddit</Form.Label>
                    <Form.Control name="subreddit" as="select" select value={this.state.value} onChange={this.handleChange}>
                        <option>2007Scape</option>
                        <option>The_donald</option>
                        <option>Nest</option>
                        <option>Wolves</option>
                        <option>Ourpresident</option>
                    </Form.Control>
                    </div>

                <Row> 
                    <br></br>
                    <br></br>
                </Row>

                

                <Form.Label>Select Date to Analyze</Form.Label>
                <div className='date'>
                <DatePicker
                    selected={this.state.date}
                    onSelect={this.handleSelect} //when day is clicked
                    onChange={this.handleChange} //only when value has changed
                />
                </div>

                <div className ='email_input'>
                    <br></br>
                    <br></br>
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" name="email" value={this.state.value} onChange={this.handleChange}/>
                <Form.Text className="text-muted">
                    Running analysis takes some time, we will e-mail you the results when it is ready
                </Form.Text>
                </div>

                <div className='submit_button'>
                        <br></br>
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </div>

                </Form.Group>
                </Form>                

                </Col>
            </container>
            </div>
        </React.Fragment>

        )
    }
}
export default Topic_modeling;