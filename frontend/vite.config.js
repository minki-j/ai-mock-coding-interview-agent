import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const DOCKER_BACKEND = "http://fastapi:8000";
const LOCAL_BACKEND = "http://localhost:8000";

const backendUrl = process.env.VITE_BACKEND_URL || 
  (process.env.DOCKER_ENV === "true" ? DOCKER_BACKEND : LOCAL_BACKEND);

// Log the backend URL for debugging
console.log(`Backend URL configured as: ${backendUrl}`);

const proxyEndpoints = [
  "/execute",
  "/get_interview",
  "/chat",
  "/init_interview",
  "/add_user",
  "/get_history",
  "/delete_all_history",
  "/update_code_editor_state",
  "/change_step",
];

const proxyConfig = Object.fromEntries(
  proxyEndpoints.map((endpoint) => [
    endpoint,
    {
      target: backendUrl,
      changeOrigin: true,
    },
  ])
);

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: proxyConfig,
    port: process.env.PORT || 3001,
    host: true,
  },
});
