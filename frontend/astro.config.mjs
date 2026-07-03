import { defineConfig } from "astro/config";

export default defineConfig({
  server: {
    port: Number(process.env.FRONTEND_PORT || 4321),
  },
});
