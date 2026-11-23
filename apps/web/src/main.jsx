import React from 'react';
import { createRoot } from 'react-dom/client';
import OrderApp from '../../../domains/order/frontend/OrderApp.jsx';
createRoot(document.getElementById('root')).render(<React.StrictMode><OrderApp /></React.StrictMode>);
