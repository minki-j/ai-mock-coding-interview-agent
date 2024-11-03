import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const backendUrl = "http://localhost:8000";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/execute': {
        target: backendUrl,
        changeOrigin: true,
      },
      '/chat': {
        target: backendUrl,
        changeOrigin: true,
      },
    },
  },
})
