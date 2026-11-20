import { describe, it, expect } from "vitest";
import { browserCapabilities } from "./api";

describe("browserCapabilities", () => {
  it("returns booleans", () => {
    const c = browserCapabilities();
    expect(typeof c.webusb).toBe("boolean");
    expect(typeof c.webcodecs).toBe("boolean");
  });
});
