import React from 'react';
import {List, Header} from 'semantic-ui-react';


export const Orders = ({ orders }) => {

    console.log('yo');
    console.log(orders);

    return (
        <List>
            {orders.map(order => {
                return(
                    <List.Item key={order.id}>
                        <Header>{order.id}</Header>
                    </List.Item>
                )
            })}
        </List>
    )
}