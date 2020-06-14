import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Home from './components/Home';
import Buyer from './components/Buyer';
import Seller from './components/Seller';
import Confirm from './components/Confirm';
import Error from './components/Error';
import Cancel from './components/Cancel';

class App extends Component {
  render() {
    return (
       <BrowserRouter>
        <div>
            <Switch>
             <Route path="/" component={Home} exact/>
             <Route path="/buyer" component={Buyer}/>
             <Route path="/seller" component={Seller}/>
             <Route path="/confirm" component={Confirm}/>
             <Route path="/cancel" component={Cancel}/>
             <Route component={Error}/>
           </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
