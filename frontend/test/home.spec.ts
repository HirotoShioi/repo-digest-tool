import { test, expect } from 'vitest';
import { page } from './setup/test-setup';

async function wait(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

test('should capture screenshot of home page', async () => {
  try {
    await page.goto('http://localhost:5173');
    
    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Ensure screenshots directory exists
    await page.screenshot({ 
      path: 'screenshots/home.png',
      fullPage: true 
    });
    
    const title = await page.title();
    expect(title).toBe('Repo Digest Tool');
  } catch (error) {
    console.error('Screenshot test failed:', error);
    throw error;
  }
});

test('should open modal when clicking Add Repository button', async () => {
  try {
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');

    // Wait for the button to be visible and clickable
    // wait for 1 second
    const addButton = page.getByRole('button', { name: 'Add Repository' });
    await addButton.waitFor({ state: 'visible' });
    await addButton.click();
    
    // Wait for modal to appear and verify it's visible
    await wait(2000);
    const modal = page.getByRole('dialog');
    await modal.waitFor({ state: 'visible' });
    expect(await modal.isVisible()).toBe(true);
    await page.screenshot({ path: 'screenshots/home-add-repository-modal.png' });
  } catch (error) {
    console.error('Modal test failed:', error);
    throw error;
  }
});

test("should clone repository", async () => {
  await page.goto("http://localhost:5173");
  await page.waitForLoadState("networkidle");
  const addButton = page.getByRole('button', { name: 'Add Repository' });
  await addButton.waitFor({ state: 'visible' });
  await addButton.click();
  const modal = page.getByRole('dialog');
  await modal.waitFor({ state: 'visible' });
  expect(await modal.isVisible()).toBe(true);
  // input repository name
  const repositoryNameInput = page.getByLabel('Repository URL');
  await repositoryNameInput.waitFor({ state: 'visible' });
  await repositoryNameInput.fill('https://github.com/HirotoShioi/repo-digest-tool');
  // click clone button
  const cloneButton = page.getByRole('button', { name: 'Clone Repository' });
  await cloneButton.waitFor({ state: 'visible' });
  await cloneButton.click();
  await page.waitForLoadState("networkidle");
});


test("should capture screenshot of repository detail page", async () => {
  await page.goto("http://localhost:5173/HirotoShioi/repo-digest-tool");
  await page.waitForLoadState("networkidle");
  await page.screenshot({ path: "screenshots/repository-detail.png", fullPage: true });
  const title = await page.title();
  expect(title).toBe("Repo Digest Tool");
});

test('should capture screenshot of filter dialog', async () => {
  await page.goto("http://localhost:5173/HirotoShioi/repo-digest-tool");
  await page.waitForLoadState("networkidle");
  
  // ビューポートのサイズを大きくする
  await page.setViewportSize({ width: 1280, height: 1024 });
  
  const filterButton = page.getByTestId('filter-dialog-button');
  
  await filterButton.waitFor({ state: 'visible' });
  await filterButton.click();
  await page.waitForLoadState("networkidle");
  await wait(2000);
  
  // ダイアログ要素を取得して、その位置とサイズを確認
  const dialog = page.getByRole('dialog');
  await dialog.waitFor({ state: 'visible' });
  
  await page.screenshot({ 
    path: "screenshots/filter-dialog.png",
  });
});
