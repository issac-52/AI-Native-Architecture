import { cancelOrder } from '../../../shared/api/orders.js';
export default function CancelOrderButton({ id, disabled, onCancelled, onError }) {
  async function cancel() {
    try { await cancelOrder(id); await onCancelled(); }
    catch(e) { onError(e.message); }
  }
  return <button type="button" disabled={disabled} onClick={cancel}>Cancel</button>;
}
