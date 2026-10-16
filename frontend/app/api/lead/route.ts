import { apiFetch, hasBackend } from "@/lib/api/config";
import { leadApiSchema } from "@/lib/schemas/lead";

export async function POST(request: Request): Promise<Response> {
  let raw: unknown;
  try {
    raw = await request.json();
  } catch {
    return Response.json(
      { error: { code: "validation_error", message: "Некорректный JSON", details: [] } },
      { status: 422 },
    );
  }

  const parsed = leadApiSchema.safeParse(raw);
  if (!parsed.success) {
    return Response.json(
      {
        error: {
          code: "validation_error",
          message: "Ошибка валидации",
          details: parsed.error.issues.map((issue) => ({
            loc: ["body", ...issue.path.map(String)],
            msg: issue.message,
            type: issue.code,
          })),
        },
      },
      { status: 422 },
    );
  }

  if (!hasBackend()) {
    console.warn("[bff] API_INTERNAL_BASE_URL не задан — заявка принята в мок-режиме");
    return Response.json({ id: 0, duplicate: false }, { status: 201 });
  }

  const upstream = await apiFetch("/api/v1/lead", {
    method: "POST",
    body: JSON.stringify(parsed.data),
  });
  if (!upstream) {
    return Response.json(
      { error: { code: "internal_error", message: "Backend недоступен", details: null } },
      { status: 502 },
    );
  }

  return new Response(await upstream.text(), {
    status: upstream.status,
    headers: { "Content-Type": "application/json" },
  });
}
