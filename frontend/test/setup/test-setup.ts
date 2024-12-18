import { beforeAll, afterAll, afterEach } from 'vitest';
import { chromium, Browser, Page } from '@playwright/test';

let browser: Browser;
export let page: Page;

beforeAll(async () => {
  // Launch browser
  browser = await chromium.launch({
    headless: true // Set to false if you want to see the browser while testing
  });
  
  // Create a new page
  const context = await browser.newContext();
  page = await context.newPage();
});

afterEach(async () => {
  // Clear any dialog handlers
  page.unroute('**/*');
});

afterAll(async () => {
  // Close browser after all tests
  await browser.close();
});
