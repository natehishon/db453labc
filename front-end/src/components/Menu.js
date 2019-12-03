import React from 'react';
import {Container, Image, Menu} from 'semantic-ui-react';

export default () => (
    <Menu>
        <Container>
            {/*<Menu.Item as="a" header>*/}
            {/*  <Image*/}
            {/*    size="small"*/}
            {/*    src="https://www.robinwieruch.de/img/page/logo.svg"*/}
            {/*  />*/}
            {/*</Menu.Item>*/}
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