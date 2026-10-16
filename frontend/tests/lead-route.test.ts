import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "@/app/api/lead/route";

function makeRequest(body: unknown): Request {
  return new Request("http://localhost/api/lead", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

const validBody = {
  name: "Иван",
  phone_number: "+375291234567",
  interest: "subscription",
  product_id: null,
  comment: null,
  source: { utm_source: "yandex" },
};

describe("POST /api/lead", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("без backend отвечает мок-успехом 201", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "");
    vi.spyOn(console, "warn").mockImplementation(() => {});
    const response = await POST(makeRequest(validBody));
    expect(response.status).toBe(201);
    await expect(response.json()).resolves.toEqual({ id: 0, duplicate: false });
  });

  it("отклоняет невалидное тело с конвертом ошибок", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "");
    const response = await POST(makeRequest({ ...validBody, interest: "other" }));
    expect(response.status).toBe(422);
    const body = await response.json();
    expect(body.error.code).toBe("validation_error");
    expect(body.error.details[0].loc).toContain("interest");
  });

  it("отклоняет битый JSON", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "");
    const response = await POST(
      new Request("http://localhost/api/lead", { method: "POST", body: "{" }),
    );
    expect(response.status).toBe(422);
  });

  it("релеит ответ backend", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(Response.json({ id: 7, duplicate: true }, { status: 200 })),
    );
    const response = await POST(makeRequest(validBody));
    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ id: 7, duplicate: true });
  });

  it("отвечает 502, когда backend недоступен", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network")));
    vi.spyOn(console, "warn").mockImplementation(() => {});
    const response = await POST(makeRequest(validBody));
    expect(response.status).toBe(502);
  });
});
