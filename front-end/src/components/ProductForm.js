import React, {useState} from 'react';
import { Form, Input, Button } from 'semantic-ui-react';

export const ProductForm = () => {

    const [title, setTitle] = useState("");

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
                     const response = await fetch('/')
                 }}>submit</Button>
            </Form.Field>
        </Form>
    )
}