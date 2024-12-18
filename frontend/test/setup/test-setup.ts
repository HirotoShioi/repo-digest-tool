import { beforeAll, afterAll, afterEach } from "vitest";
import { chromium, Browser, Page } from "@playwright/test";
import path from "path";
import fs from "fs";
let browser: Browser;
export let page: Page;

beforeAll(async () => {
  const screenshotsDir = path.join(process.cwd(), "screenshots");

  // Create screenshots directory if it doesn't exist
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  } else {
    // Clean up existing screenshots
    const files = fs.readdirSync(screenshotsDir);
    for (const file of files) {
      fs.unlinkSync(path.join(screenshotsDir, file));
    }
  }
  // Launch browser
  browser = await chromium.launch({
    headless: true, // Set to false if you want to see the browser while testing
  });

  // Create a new page
  const context = await browser.newContext();
  page = await context.newPage();
});

afterEach(async () => {
  // Clear any dialog handlers
  page.unroute("**/*");
});

afterAll(async () => {
  // Close browser after all tests
  await browser.close();
});
