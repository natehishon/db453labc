import React, {useState, useEffect} from "react";
import {Header} from 'semantic-ui-react';
import axios from 'axios';


export const Orders = ({orderId}) => {


    const [order, setOrder] = useState();

    useEffect(() => {
        axios
            .get(
                "/products"+orderId
            )
            .then(({data}) => {

            })
    }

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