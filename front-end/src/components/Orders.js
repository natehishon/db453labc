import React from 'react';
import {List, Header} from 'semantic-ui-react';


export const Orders = ({ orders }) => {

    return (
        <List>
            {orders.map(order => {
                return(
                    <List.Item key={order.id}>
                        <Header>{order.date_posted}</Header>
                    </List.Item>
                )
            })}
        </List>
    )
}