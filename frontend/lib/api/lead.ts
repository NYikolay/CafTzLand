import type { LeadFieldErrors, LeadResult } from "@/lib/types";

export const GENERIC_LEAD_ERROR =
  "Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.";

const FIELD_NAMES = ["name", "phone_number", "interest", "product_id", "comment"] as const;

type BackendErrorBody = {
  error?: {
    code?: string;
    message?: string;
    details?: Array<{ loc?: Array<string | number>; msg?: string }> | null;
  };
};

export function interpretLeadResponse(status: number, body: unknown): LeadResult {
  if (status === 201 || status === 200) {
    const data = body as { id?: unknown; duplicate?: unknown } | null;
    if (typeof data?.id === "number") {
      return data.duplicate === true
        ? { status: "duplicate", id: data.id }
        : { status: "created", id: data.id };
    }
    return { status: "error", message: GENERIC_LEAD_ERROR };
  }

  if (status === 422) {
    const data = body as BackendErrorBody | null;
    const fieldErrors: LeadFieldErrors = {};
    for (const detail of data?.error?.details ?? []) {
      const loc = detail.loc ?? [];
      let field: (typeof FIELD_NAMES)[number] | undefined;
      for (let index = loc.length - 1; index >= 0; index -= 1) {
        const part = loc[index];
        if (typeof part === "string" && (FIELD_NAMES as readonly string[]).includes(part)) {
          field = part as (typeof FIELD_NAMES)[number];
          break;
        }
      }
      if (field && detail.msg && !(field in fieldErrors)) {
        fieldErrors[field] = detail.msg;
      }
    }
    return { status: "validation", fieldErrors };
  }

  return { status: "error", message: GENERIC_LEAD_ERROR };
}
