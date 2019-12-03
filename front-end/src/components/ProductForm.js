import React, {useState} from 'react';
import { Form, Input, Button } from 'semantic-ui-react';

export const ProductForm = () => {

    const [title, setTitle] = useState("")  ;

    return (
        <Form>
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

                     }

                 }}>submit</Button>
            </Form.Field>
        </Form>
    )
}