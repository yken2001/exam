import { execSync } from 'node:child_process'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

// which build a device is running -- written into exported records so a
// problem report can be matched to the exact code and question bank
function appVersion(): string {
  const date = new Date().toISOString().slice(0, 10)
  try {
    return `${execSync('git rev-parse --short HEAD').toString().trim()} (${date})`
  } catch {
    return date
  }
}

// https://vite.dev/config/
export default defineConfig({
  define: { __APP_VERSION__: JSON.stringify(appVersion()) },
  // relative base + inlined JS/CSS (no type="module") so the built dist/index.html
  // can be opened directly via file:// in Chrome, with no dev/preview server.
  // public/questions & public/explanations stay as plain files, referenced by
  // relative <img src>, which file:// allows even though it blocks ES modules.
  base: './',
  plugins: [react(), viteSingleFile({ removeViteModuleLoader: true })],
})
