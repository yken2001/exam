import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

// https://vite.dev/config/
export default defineConfig({
  // relative base + inlined JS/CSS (no type="module") so the built dist/index.html
  // can be opened directly via file:// in Chrome, with no dev/preview server.
  // public/questions & public/explanations stay as plain files, referenced by
  // relative <img src>, which file:// allows even though it blocks ES modules.
  base: './',
  plugins: [react(), viteSingleFile({ removeViteModuleLoader: true })],
})
