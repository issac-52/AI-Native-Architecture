import React from 'react';
import { createRoot } from 'react-dom/client';
import { OrdersPage } from '../pages/orders';
import './styles.css';
createRoot(document.getElementById('root')).render(<React.StrictMode><OrdersPage /></React.StrictMode>);
