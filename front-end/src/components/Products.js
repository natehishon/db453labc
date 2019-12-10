import React from 'react';
import {List, Header} from 'semantic-ui-react';


export const Products = ({ products }) => {

    return (
        <List>
            {products.map(product => {
                return(
                    <List.Item key={product.title}>
                        <Header>{product.title}</Header>
                    </List.Item>
                )
            })}
        </List>
    )
}