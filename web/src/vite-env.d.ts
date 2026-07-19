/// <reference types="vite/client" />

/**
 * Client-visible environment variables must use the VITE_ prefix.
 * Vite only exposes VITE_* to browser code; other env vars stay server-side.
 * Do not place secrets, credentials, or operational endpoints here.
 */
interface ImportMetaEnv {
  readonly VITE_APP_TITLE?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
