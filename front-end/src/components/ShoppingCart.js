import React, {useState, useEffect} from "react";
import {Header} from 'semantic-ui-react';
import axios from 'axios';


export const ShoppingCart = () => {


    const [shoppingCart, setShoppingCart] = useState();

    useEffect(() => {
        axios
            .get(
                "/react-shopcart"
            )
            .then(({data}) => {
                console.log(data);
            })
    });

    return (
        <div>{}
            {/*{orders.map(order => {*/}
            {/*    return(*/}
            {/*        <List.Item key={order.id}>*/}
            {/*            <Header>{order.id}</Header>*/}
            {/*        </List.Item>*/}
            {/*    )*/}
            {/*})}*/}
        </div>
    )
}