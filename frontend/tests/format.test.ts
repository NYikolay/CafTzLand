import { describe, expect, it } from "vitest";
import { formatByn } from "@/lib/format";

describe("formatByn", () => {
  it.each([
    ["26.00", "26 BYN"],
    ["26.50", "26.50 BYN"],
    ["48.00", "48 BYN"],
  ])("%s -> %s", (input, expected) => {
    expect(formatByn(input)).toBe(expected);
  });
});
