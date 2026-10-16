import { describe, expect, it } from "vitest";
import { leadApiSchema, leadFormSchema, toLeadApiPayload } from "@/lib/schemas/lead";

describe("leadFormSchema", () => {
  const valid = {
    interest: "subscription" as const,
    name: "Иван",
    phone_number: "+375 (29) 123-45-67",
    comment: "",
    product_id: "",
  };

  it("принимает корректные значения", () => {
    expect(leadFormSchema.safeParse(valid).success).toBe(true);
  });

  it("требует имя", () => {
    const result = leadFormSchema.safeParse({ ...valid, name: "   " });
    expect(result.success).toBe(false);
  });

  it("даёт текст ошибки телефона из макета", () => {
    const result = leadFormSchema.safeParse({ ...valid, phone_number: "залупа" });
    expect(result.success).toBe(false);
    if (!result.success) {
      const issue = result.error.issues.find((i) => i.path[0] === "phone_number");
      expect(issue?.message).toBe("Пожалуйста, введите корректный номер телефона");
    }
  });

  it("ограничивает комментарий 2000 символами", () => {
    const result = leadFormSchema.safeParse({ ...valid, comment: "x".repeat(2001) });
    expect(result.success).toBe(false);
  });
});

describe("leadApiSchema", () => {
  it("принимает полное тело", () => {
    const result = leadApiSchema.safeParse({
      name: "Иван",
      phone_number: "+375291234567",
      interest: "one_time",
      product_id: 3,
      comment: null,
      source: { utm_source: "yandex" },
    });
    expect(result.success).toBe(true);
  });
  it("отклоняет неизвестный интерес", () => {
    const result = leadApiSchema.safeParse({
      name: "Иван",
      phone_number: "+375291234567",
      interest: "other",
    });
    expect(result.success).toBe(false);
  });
});

describe("toLeadApiPayload", () => {
  it("нормализует телефон и продукт", () => {
    const payload = toLeadApiPayload({
      interest: "subscription",
      name: "  Иван ",
      phone_number: "+375 (29) 123-45-67",
      comment: "",
      product_id: "4",
    });
    expect(payload).toEqual({
      name: "Иван",
      phone_number: "+375291234567",
      interest: "subscription",
      product_id: 4,
      comment: null,
    });
  });
});
