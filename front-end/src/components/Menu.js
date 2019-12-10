import React from 'react';
import {Container, Image, Menu} from 'semantic-ui-react';

export default () => (
    <Menu>
        <Container>

            <Menu.Menu position="right">
                <Menu.Item as="a" name="login">
                    Cart
                </Menu.Item>
                <Menu.Item as="a" name="login">
                    Orders
                </Menu.Item>
                <Menu.Item as="a" name="register">
                    Products
                </Menu.Item>
            </Menu.Menu>
        </Container>
    </Menu>
);