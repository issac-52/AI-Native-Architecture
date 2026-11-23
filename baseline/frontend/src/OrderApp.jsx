import { useEffect, useState } from 'react';
import './style.css';

export default function OrderApp() {
  const [items, setItems] = useState([]);
  const [productName, setProductName] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState('');

  async function request(path, options) {
    const response = await fetch(path, options);
    if (!response.ok) throw new Error(`Request failed (HTTP ${response.status})`);
    return response.json();
  }

  async function reload() {
    try { setItems(await request('/api/orders')); setError(''); }
    catch (e) { setError(e.message); }
  }
  useEffect(() => { reload(); }, []);

  async function create(event) {
    event.preventDefault();
    try {
      await request('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ productName, quantity: Number(quantity) })
      });
      setProductName('');
      await reload();
    } catch (e) { setError(e.message); }
  }

  async function cancel(id) {
    try {
      await request(`/api/orders/${id}/cancel`, { method: 'POST' });
      await reload();
    } catch (e) { setError(e.message); }
  }

  return (
    <main>
      <header><span className="eyebrow">Architecture research prototype</span><h1>Order management</h1><p>Same features, different source layout. Data resets on backend restart.</p></header>
      <section>
        <h2>Create order</h2>
        <form onSubmit={create}>
          <label>Product <input aria-label="Product" value={productName} onChange={e => setProductName(e.target.value)} required /></label>
          <label>Quantity <input aria-label="Quantity" type="number" min="1" value={quantity} onChange={e => setQuantity(e.target.value)} required /></label>
          <button type="submit">Create</button>
        </form>
      </section>
      {error && <p role="alert" className="error">{error}</p>}
      <section><div className="heading"><h2>Orders</h2><button type="button" className="secondary" onClick={reload}>Refresh</button></div>
        {items.length === 0 ? <p>No orders yet.</p> : <ul>{items.map(item =>
          <li key={item.id}><div><strong>#{item.id} — {item.productName}</strong><small>Qty {item.quantity} · {item.status}</small></div>
            <button disabled={item.status === 'CANCELLED'} onClick={() => cancel(item.id)}>Cancel</button></li>
        )}</ul>}
      </section>
    </main>
  );
}
