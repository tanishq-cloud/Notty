import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.getByRole('button', { name: 'Get Started' }).click();
  await expect(page).toHaveTitle(/Notty/);
});

test('get started link', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.getByRole('button', { name: 'Get started' }).click();
  await expect(page.getByRole('heading', { name: 'Create an account' })).toBeVisible();
});
// Helper function for common login flow
async function login(page, username: string, password: string) {
  await page.goto('http://localhost:3000/login');
  await page.getByRole('textbox', { name: 'Username' }).fill(username);
  await page.getByRole('textbox', { name: 'Password' }).fill(password);
  await page.getByRole('button', { name: 'Sign in' }).click();
}

test.describe('Notty App Login and Registration Tests', () => {
  test('should register new user successfully', async ({ page }) => {
    await page.goto('http://localhost:3000/register');
    await page.getByRole('textbox', { name: 'Full Name' }).fill('Test User12');
    await page.getByRole('textbox', { name: 'Username' }).fill('testuser1234');
    await page.getByRole('textbox', { name: 'Password' }).fill('password123');
    await page.getByRole('button', { name: 'Create account' }).click();
    await expect(page.getByText('Registration successful!')).toBeVisible();
  });

  test('should register show error for old user', async ({ page }) => {
    await page.goto('http://localhost:3000/register');
    await page.getByRole('textbox', { name: 'Full Name' }).fill('Test User1');
    await page.getByRole('textbox', { name: 'Username' }).fill('testuser123');
    await page.getByRole('textbox', { name: 'Password' }).fill('password123');
    await page.getByRole('button', { name: 'Create account' }).click();
    await expect(page.getByText('Registration failed. Please')).toBeVisible();
  });

  test('should login successfully', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    await expect(page.getByRole('heading', { name: 'My Notes' })).toBeVisible();
  });

  test('should throw error for invalid login ', async ({ page }) => {
    await login(page, 'testuser12', 'password123');
    await expect(page.getByText('Invalid username or password')).toBeVisible();
  });
})


test.describe('Notty App Note Tests', () => {

  test('should create a new note', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    await page.getByTestId('create-button').click();
    await page.getByRole('textbox', { name: 'Title' }).fill('Test Note');
    await page.getByTestId('quill-editor').locator('div').filter({ hasText: 'Start writing here....' }).fill('This is a test note');
    await page.getByRole('button', { name: 'Create Note' }).click();
    await expect(page.getByText('New Note created successfully!')).toBeVisible();
  });

  test('should edit an existing note', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    await page.getByTestId('edit-button').nth(2).click();
    await page.getByTestId('quill-editor').locator('div').first().fill('Updated note content');
    await page.getByRole('button', { name: 'Update Note' }).click();
    await expect(page.getByText('Note updated successfully!')).toBeVisible();
  });

  test('should view note details', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    await page.getByTestId('view-button').nth(2).click();
    await expect(page.getByRole('heading', { name: 'View Note' })).toBeVisible();
    await page.locator('button[type="button"]').filter({ hasText: 'Close' }).first().click();
    await expect(page.getByRole('heading', { name: 'My Notes' })).toBeVisible();
    await expect(page.locator('div').filter({ hasText: /^Note: Test Note$/ }).first()).toBeVisible;
  });

  test('should delete note', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    await page.getByTestId('delete-button').nth(2).click();
    await expect(page.getByRole('heading', { name: 'Are you sure?' })).toBeVisible();
    await page.getByRole('button', { name: 'Delete' }).click();
    await expect(page.getByText('No note has been created')).toBeVisible();
    // Add assertion for successful deletion message if available
  });

  test('should logout successfully', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    await page.getByRole('button', { name: 'Logout' }).click();
    await expect(page.getByRole('heading', { name: 'Sign in to your account' })).toBeVisible();
  });

  test('should handle invalid login', async ({ page }) => {
    await page.goto('http://localhost:3000/login');
    await page.getByRole('textbox', { name: 'Username' }).fill('wronguser');
    await page.getByRole('textbox', { name: 'Password' }).fill('wrongpass');
    await page.getByRole('button', { name: 'Sign in' }).click();
    // Add assertion for error message if available
  });

  test('update disable', async ({ page }) => {
    await login(page, 'testuser', 'password123');
    

    //testing update button is disable.
    await page.locator('div').filter({ hasText: /^This is a test note for update test hjkdfjkjdEdit$/ }).getByTestId('edit-button').click();
    await expect(page.getByText('CancelUpdate Note')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Update Note' })).toBeDisabled();
    
    await page.getByTestId('quill-editor').getByText('This is a test note for').click();
    await page.getByTestId('quill-editor').locator('div').filter({ hasText: 'This is a test note for' }).fill('This is a test note for update test hjkdfjkjd , new data');
    await page.getByRole('button', { name: 'Update Note' }).click();
    await page.getByText('Note updated successfully!').click();
  });

});