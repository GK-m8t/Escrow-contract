import React, { Component } from 'react';
import { Link } from 'react-router-dom';


export default class Home extends Component {
  render() {
    return (
    <div class='index'>
       <Link to={"/seller" }>Sell your guitar</Link>
       <br/><br/>
       <Link to={"/buyer" }>Buy a guitar</Link>
       <br/><br/>
       <Link to={"/confirm" }>confirm that you have recieved the guitar from the seller</Link>
       <br/><br/>
       <Link to={"/cancel" }>Cancel the sell order you have initiated</Link>
       <br/><br/>
    </div>
    )
  }
}
