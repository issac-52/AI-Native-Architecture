import { useState } from 'react';
import { createOrder } from '../../../shared/api/orders.js';
export default function CreateOrderForm({ onCreated, onError }) {
  const [productName, setProductName] = useState('');
  const [quantity, setQuantity] = useState(1);
  async function submit(event) {
    event.preventDefault();
    try {
      await createOrder({ productName, quantity: Number(quantity) });
      setProductName('');
      await onCreated();
    } catch(e) { onError(e.message); }
  }
  return <form onSubmit={submit}>
    <label>Product <input aria-label="Product" value={productName} onChange={e=>setProductName(e.target.value)} required/></label>
    <label>Quantity <input aria-label="Quantity" type="number" min="1" value={quantity} onChange={e=>setQuantity(e.target.value)} required/></label>
    <button type="submit">Create</button>
  </form>;
}
