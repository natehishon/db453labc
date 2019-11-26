import React, {useEffect, useState} from 'react';
import './App.css';
import {Products} from "./components/Products";
import {ProductForm} from "./components/ProductForm";
import {Container} from "semantic-ui-react";

function App() {

    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch('/products').then(response => {
            response.json().then(data => {
                console.log(data);
                setProducts(data.results);
            })
        })
    }, [])

    return (
        <div className="App">

            <Container>
                <ProductForm/>
                <Products products={products}></Products>
            </Container>


        </div>
    );
}

export default App;
