import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // Allow external access (important for Docker and Render)
    open: true,
    strictPort: false,
  },
});
