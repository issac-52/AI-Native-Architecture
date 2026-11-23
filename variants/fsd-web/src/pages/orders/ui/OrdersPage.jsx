import { useEffect, useState } from 'react';
import { fetchOrders } from '../../../shared/api/orders.js';
import { CreateOrderForm } from '../../../features/create-order';
import { CancelOrderButton } from '../../../features/cancel-order';
import { OrderList } from '../../../entities/order';

/** A page composes feature/entity public APIs. */
export default function OrdersPage() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');
  async function reload() {
    try { setItems(await fetchOrders()); setError(''); }
    catch(e) { setError(e.message); }
  }
  useEffect(() => { reload(); }, []);
  return <main>
    <header><span className="eyebrow">Feature-Sliced Design reference</span><h1>Order management</h1>
      <p>Same order API; React organized by app / pages / features / entities / shared.</p></header>
    <section><h2>Create order</h2><CreateOrderForm onCreated={reload} onError={setError}/></section>
    {error && <p role="alert" className="error">{error}</p>}
    <section><div className="heading"><h2>Orders</h2><button type="button" className="secondary" onClick={reload}>Refresh</button></div>
      <OrderList orders={items} actions={order =>
        <CancelOrderButton id={order.id} disabled={order.status === 'CANCELLED'}
          onCancelled={reload} onError={setError}/>}
      />
    </section>
  </main>;
}
