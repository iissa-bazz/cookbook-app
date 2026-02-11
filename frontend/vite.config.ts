import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Needed for Docker
    port: 5173,
    proxy: {
      // This matches the baseURL: '/api' in the axios client
      '/api': {
        target: 'http://backend:8000', // FastAPI backend
        changeOrigin: true,
        // strips the '/api' prefix before sending it to the backend so '/api/recipes/suggestions' becomes '/recipes/suggestions'
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})