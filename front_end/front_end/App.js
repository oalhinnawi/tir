import React from 'react';
import Home from './Home.js';
import Faq from './Faq.js';
import Topic_modeling from './Topic_modeling.js'
import './App.css';
import { BrowserRouter as Router, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
   
  return (

      <Router>
        <div>
          <Route exact path="/" component={Home} />
          <Route path="/Faq" component={Faq} />
          <Route path="/Topic_modeling" component={Topic_modeling} />
        </div>
      </Router>
    )
      
  }

export default App;
