async function request(path, options) {
  const response = await fetch(path, options);
  if (!response.ok) throw new Error(`Request failed (HTTP ${response.status})`);
  return response.json();
}
export function fetchOrders() { return request('/api/orders'); }
export function cancelOrder(id) { return request(`/api/orders/${id}/cancel`, {method:'POST'}); }
export function createOrder(order) {
  return request('/api/orders', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(order)});
}
