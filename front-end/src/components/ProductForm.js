import React, {useState} from 'react';
import {Form, Input, Button} from 'semantic-ui-react';

export const ProductForm = () => {

    const [title, setTitle] = useState("");

    let formStyle = {
        width: '300px',
        margin: '100px auto'
    }

    let labelStyle = {
        'font-size': '18px',
        margin: '20px 0',
    };

    return (
        <Form style={formStyle}>
            <div style={labelStyle}>
                <label>PC's Tuna Emporium Product Form</label>
            </div>
            <Form.Field>
                <Input
                    placeholder="Product Title"
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                />
            </Form.Field>
            <Form.Field>
                <Button onClick={async () => {
                    const product = {title};
                    const response = await fetch('/add_product', {
                        method: 'POST',
                        headers: {
                            'Content-type': 'application/json'
                        },
                        body: JSON.stringify(product)
                    })


                    if (response.ok) {
                        console.log(response);
                        console.log("good!");
                        setTitle("");
                    }

                }}>submit</Button>
            </Form.Field>
        </Form>
    )
}