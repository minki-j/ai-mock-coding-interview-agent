import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const backendUrl = "http://localhost:8000";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/execute": {
        target: backendUrl,
        changeOrigin: true,
      },
      "/get_interview": {
        target: backendUrl,
        changeOrigin: true,
      },
      "/chat": {
        target: backendUrl,
        changeOrigin: true,
      },
      "/init_interview": {
        target: backendUrl,
        changeOrigin: true,
      },
      "/add_user": {
        target: backendUrl,
        changeOrigin: true,
      },
    },
    host: true,
    port: 3001,
  },
});