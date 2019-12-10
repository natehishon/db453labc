import React, {useEffect, useState, Component} from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom';
import './App.css';
import {Products} from "./components/Products";
import {Orders} from "./components/Orders";
import {ProductForm} from "./components/ProductForm";
import Menu from './components/Menu';
import {Container} from "semantic-ui-react";
import {ShoppingCart} from "./components/ShoppingCart";


function App() {

    const [products, setProducts] = useState([]);
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        fetch('/react-products').then(response => {
            response.json().then(data => {
                console.log(data);
                setProducts(data.results);
            })
        })
        fetch('/react-orders').then(response => {
            response.json().then(data => {
                console.log(data);
                setOrders(data.orders);
            })
        })
    }, [])

    return (
        <div className="App">


            <Router>
                <div>
                    {/*style this*/}
                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                        <ul className="navbar-nav mr-auto">
                            <li><Link to={'/products'} className="nav-link"> Products </Link></li>
                            <li><Link to={'/orders'} className="nav-link"> Orders </Link></li>
                            <li><Link to={'/product-form'} className="nav-link">Product Form</Link></li>
                            {/*<li><Link to={'/shopping-cart'} className="nav-link">Shopping Cart</Link></li>*/}
                            {/*<li><Link to={'/about'} className="nav-link">About</Link></li>*/}
                        </ul>
                    </nav>
                    <hr/>
                    <Switch>
                        {/*<Route exact path='/' component={Products}/>*/}
                        {/*<Route render={(props) => <Products products={products}>/>/>*/}
                        <Route
                            path='/products'
                            render={(props) => <Products {...props} products={products}/>}
                        />
                        <Route
                            path='/orders'
                            render={(props) => <Orders {...props} orders={orders}/>}
                        />
                        <Route
                            path='/product-form'
                            render={(props) => <ProductForm {...props} />}
                        />
                        {/*<Route*/}
                        {/*    path='/shopping-cart'*/}
                        {/*    render={(props) => <ShoppingCart {...props} />}*/}
                        {/*/>*/}
                        {/*<Route path='/contact' component={Contact}/>*/}
                        {/*<Route path='/about' component={About}/>*/}
                    </Switch>
                </div>
            </Router>

            {/*<Menu/>*/}
            {/*<Container>*/}
            {/*    <ProductForm />*/}
            {/*    <Products products={products}></Products>*/}
            {/*</Container>*/}


        </div>
    );
}

export default App;
