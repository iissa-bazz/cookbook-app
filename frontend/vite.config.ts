import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '')
  // Log this to your terminal so you can see what Vite is seeing
  console.log('--- Vite Proxy Target:', env.VITE_API_TARGET || 'http://localhost:8000 (Default)');

  return {
    plugins: [react()],
    server: {
      host: true,
      port: 5173,
      proxy: {
        '/api': {
          // Use the environment variable, defaulting to local if not set
          target: env.VITE_API_TARGET || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  }
})