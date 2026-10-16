import { describe, expect, it } from "vitest";
import { formatByPhone, isValidByPhone, normalizeByPhone } from "@/lib/phone";

describe("normalizeByPhone", () => {
  it.each([
    ["+375 (29) 123-45-67", "+375291234567"],
    ["375291234567", "+375291234567"],
    ["80 29 1234567", "+375291234567"],
    ["(029) 1234567", "+375291234567"],
    ["+375 (17) 123-45-67", "+375171234567"],
  ])("нормализует %s", (input, expected) => {
    expect(normalizeByPhone(input)).toBe(expected);
  });

  it.each([["залупа"], ["+375 29"], [""], ["+7 999 123-45-67"]])(
    "отклоняет %s",
    (input) => {
      expect(normalizeByPhone(input)).toBeNull();
      expect(isValidByPhone(input)).toBe(false);
    },
  );
});

describe("formatByPhone", () => {
  it("форматирует полный номер", () => {
    expect(formatByPhone("291234567")).toBe("+375 (29) 123-45-67");
  });
  it("форматирует частичный ввод", () => {
    expect(formatByPhone("29")).toBe("+375 (29)");
    expect(formatByPhone("29123")).toBe("+375 (29) 123");
  });
  it("понимает национальный префикс", () => {
    expect(formatByPhone("80291234567")).toBe("+375 (29) 123-45-67");
  });
});
