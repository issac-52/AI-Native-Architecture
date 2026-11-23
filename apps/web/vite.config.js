import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
export default defineConfig({
  plugins: [react()],
  resolve: {
    // A domain module is outside apps/web: resolve React from the web app,
    // not from the domain's nearest node_modules directory.
    dedupe: ['react', 'react-dom']
  },
  server: {
    port: 5173,
    fs: { allow: [fileURLToPath(new URL('../../', import.meta.url))] },
    proxy: { '/api': 'http://localhost:8080' }
  }
});
