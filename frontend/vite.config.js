import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

console.log("process.env.DOCKER_ENV:", process.env.DOCKER_ENV);
const running_on_docker = process.env.DOCKER_ENV === "true";
const backendUrl = running_on_docker
  ? "http://fastapi:8000"
  : "http://localhost:8000";

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
    host: true,
    port: 3001,
  },
});
