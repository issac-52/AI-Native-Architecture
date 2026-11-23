export default function OrderList({ orders, actions }) {
  if (orders.length === 0) return <p>No orders yet.</p>;
  return <ul>{orders.map(item => <li key={item.id}>
    <div><strong>#{item.id} — {item.productName}</strong><small>Qty {item.quantity} · {item.status}</small></div>
    {actions(item)}
  </li>)}</ul>;
}
