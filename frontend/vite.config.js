import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const running_on_docker = process.env.DOCKER_ENV === 'true';
const backendUrl = running_on_docker ? "http://fastapi:8000" : "http://localhost:8000";

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
      "/get_history": {
        target: backendUrl,
        changeOrigin: true,
      },
      "/delete_all_history": {
        target: backendUrl,
        changeOrigin: true,
      },
    },
    host: true,
    port: 3001,
  },
});

// 67309a27b948ea277e3af9cd