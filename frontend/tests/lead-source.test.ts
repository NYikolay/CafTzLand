import { describe, expect, it } from "vitest";
import { collectLeadSource } from "@/lib/lead-source";

describe("collectLeadSource", () => {
  it("собирает utm и page_url из window", () => {
    window.history.replaceState({}, "", "/?utm_source=yandex&utm_medium=cpc");
    const source = collectLeadSource();
    expect(source.utm_source).toBe("yandex");
    expect(source.utm_medium).toBe("cpc");
    expect(source.page_url).toBe(window.location.href);
  });
});
