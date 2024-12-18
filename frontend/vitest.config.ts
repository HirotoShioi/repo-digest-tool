import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: "happy-dom", // または適切なブラウザ環境
    setupFiles: ['./test/setup/test-setup.ts'], // Playwright設定用ファイル
  },
});
