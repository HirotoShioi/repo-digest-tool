import { test, expect } from 'vitest';
import { page } from './setup/test-setup';

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
    const addButton = page.getByRole('button', { name: 'Add Repository' });
    await addButton.waitFor({ state: 'visible' });
    await addButton.click();

    // Wait for modal to appear and verify it's visible
    const modal = page.getByRole('dialog');
    await modal.waitFor({ state: 'visible' });
    expect(await modal.isVisible()).toBe(true);
    await page.screenshot({ path: 'screenshots/home-add-repository-modal.png' });
  } catch (error) {
    console.error('Modal test failed:', error);
    throw error;
  }
});
