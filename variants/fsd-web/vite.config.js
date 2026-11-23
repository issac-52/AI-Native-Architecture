import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  server: { port: 5175, proxy: { '/api': process.env.API_TARGET || 'http://localhost:8081' } }
});
