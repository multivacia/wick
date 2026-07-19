import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

/**
 * Only variables prefixed with VITE_ are exposed to client code.
 * Never put secrets, DATABASE_URL, provider tokens, or host credentials
 * in VITE_* variables — they are embedded in the production bundle.
 */
export default defineConfig(({ mode }) => {
  // Touch loadEnv so typing/docs stay aligned with Vite env policy.
  loadEnv(mode, process.cwd(), "VITE_");

  return {
    plugins: [react()],
    build: {
      sourcemap: false,
      outDir: "dist",
      emptyOutDir: true,
    },
    server: {
      host: "127.0.0.1",
      port: 5173,
      strictPort: true,
    },
    preview: {
      host: "127.0.0.1",
      port: 4173,
      strictPort: true,
    },
  };
});
