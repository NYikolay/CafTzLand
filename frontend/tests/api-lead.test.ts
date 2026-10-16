import { describe, expect, it } from "vitest";
import { interpretLeadResponse } from "@/lib/api/lead";

describe("interpretLeadResponse", () => {
  it("201 -> created", () => {
    expect(interpretLeadResponse(201, { id: 42, duplicate: false })).toEqual({
      status: "created",
      id: 42,
    });
  });

  it("200 duplicate -> duplicate", () => {
    expect(interpretLeadResponse(200, { id: 41, duplicate: true })).toEqual({
      status: "duplicate",
      id: 41,
    });
  });

  it("422 -> fieldErrors по loc", () => {
    const body = {
      error: {
        code: "validation_error",
        message: "Ошибка валидации",
        details: [
          {
            type: "phone_invalid",
            loc: ["body", "phone_number"],
            msg: "Пожалуйста, введите корректный номер телефона",
          },
        ],
      },
    };
    expect(interpretLeadResponse(422, body)).toEqual({
      status: "validation",
      fieldErrors: {
        phone_number: "Пожалуйста, введите корректный номер телефона",
      },
    });
  });

  it("500 -> error с общим текстом", () => {
    const result = interpretLeadResponse(500, null);
    expect(result.status).toBe("error");
    if (result.status === "error") {
      expect(result.message).toBe(
        "Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.",
      );
    }
  });
});
