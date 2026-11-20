import { test, expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.route("http://127.0.0.1:8787/api/health", (route) =>
    route.fulfill({ json: { status: "ok", adb: true } })
  );
  await page.route("http://127.0.0.1:8787/api/devices", (route) =>
    route.fulfill({
      json: {
        devices: [
          {
            serial: "ABC123",
            state: "device",
            model: "Pixel",
            metadata: { model: "Pixel", android_version: "14" },
          },
        ],
      },
    })
  );
  await page.goto("/?token=test-token");
});

test("shows device", async ({ page }) => {
  await expect(page.locator("strong", { hasText: "Pixel" })).toBeVisible();
  await expect(page.getByText("device").first()).toBeVisible();
});

test("apk dropzone present", async ({ page }) => {
  await expect(page.getByText("Drop an APK here or click to choose")).toBeVisible();
});