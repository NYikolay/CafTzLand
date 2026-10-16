import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LeadForm } from "@/components/form/lead-form";
import { LeadFormProvider, useLeadForm } from "@/components/form/lead-form-context";
import { SubscribeCtaButton } from "@/components/form/subscribe-cta-button";
import { fixtureLeadOptions } from "@/lib/fixtures/lead-options";
import { fixtureProducts } from "@/lib/fixtures/products";

function renderForm() {
  return render(
    <LeadFormProvider>
      <LeadForm products={fixtureProducts} options={fixtureLeadOptions} />
    </LeadFormProvider>,
  );
}

function PresetCoffeeButton({ productId }: { productId: number }) {
  const { selectCoffee } = useLeadForm();
  return (
    <button type="button" onClick={() => selectCoffee(productId)}>
      пресет кофе
    </button>
  );
}

describe("LeadForm", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    window.history.replaceState({}, "", "/");
  });

  it("по умолчанию выбран интерес «Подписка»", () => {
    renderForm();
    expect(screen.getByRole("radio", { name: "Подписка" })).toBeChecked();
  });

  it("варианты заказа — сетка с равными ширинами", () => {
    renderForm();
    const card = screen.getByRole("radio", { name: "Вопрос" }).closest("label");
    expect(card).not.toBeNull();
    expect(card?.className).not.toContain("flex-1");
    const grid = card?.parentElement;
    expect(grid?.className).toContain("grid-cols-2");
    expect(grid?.className).toContain("lg:grid-cols-3");
  });

  it("показывает текст ошибки телефона из макета", async () => {
    const user = userEvent.setup();
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "123");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(
      await screen.findByText("Пожалуйста, введите корректный номер телефона"),
    ).toBeInTheDocument();
  });

  it("показывает подтверждение при 201", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({ id: 1, duplicate: false }, { status: 201 }),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(
      await screen.findByText("Спасибо! Заявка отправлена — менеджер перезвонит."),
    ).toBeInTheDocument();
  });

  it("показывает сообщение о дубле", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({ id: 1, duplicate: true }, { status: 200 }),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(
      await screen.findByText("Заявка уже отправлена — менеджер перезвонит"),
    ).toBeInTheDocument();
  });

  it("показывает msg от backend из 422", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json(
          {
            error: {
              code: "validation_error",
              message: "Ошибка валидации",
              details: [
                { loc: ["body", "phone_number"], msg: "Номер не обслуживается" },
              ],
            },
          },
          { status: 422 },
        ),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "375291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(await screen.findByText("Номер не обслуживается")).toBeInTheDocument();
  });

  it("пресет товара из контекста выставляет select", async () => {
    const user = userEvent.setup();
    render(
      <LeadFormProvider>
        <PresetCoffeeButton productId={4} />
        <LeadForm products={fixtureProducts} options={fixtureLeadOptions} />
      </LeadFormProvider>,
    );
    await user.click(screen.getByRole("button", { name: "пресет кофе" }));
    await waitFor(() => {
      expect(screen.getByLabelText("Какой кофе? Необязательно")).toHaveValue("4");
    });
  });

  it("пресет интереса из контекста возвращает «Подписка»", async () => {
    const user = userEvent.setup();
    render(
      <LeadFormProvider>
        <SubscribeCtaButton />
        <LeadForm products={fixtureProducts} options={fixtureLeadOptions} />
      </LeadFormProvider>,
    );
    await user.click(screen.getByRole("radio", { name: "Вопрос" }));
    expect(screen.getByRole("radio", { name: "Вопрос" })).toBeChecked();
    await user.click(screen.getByRole("button", { name: /Хочу кофе по подписке/ }));
    await waitFor(() => {
      expect(screen.getByRole("radio", { name: "Подписка" })).toBeChecked();
    });
  });

  it("показывает msg от backend для product_id из 422", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json(
          {
            error: {
              code: "validation_error",
              message: "Ошибка валидации",
              details: [
                { loc: ["body", "product_id"], msg: "Такого кофе нет", type: "value_error" },
              ],
            },
          },
          { status: 422 },
        ),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(await screen.findByText("Такого кофе нет")).toBeInTheDocument();
  });

  it("показывает msg от backend для interest из 422", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json(
          {
            error: {
              code: "validation_error",
              message: "Ошибка валидации",
              details: [
                { loc: ["body", "interest"], msg: "Подписка недоступна", type: "value_error" },
              ],
            },
          },
          { status: 422 },
        ),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(await screen.findByText("Подписка недоступна")).toBeInTheDocument();
  });

  it("показывает общую ошибку при 500", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json(
          { error: { code: "internal_error", message: "Internal server error" } },
          { status: 500 },
        ),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(
      await screen.findByText(
        "Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.",
      ),
    ).toBeInTheDocument();
  });

  it("показывает общее сообщение при 422 без деталей", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json(
          {
            error: {
              code: "validation_error",
              message: "Ошибка валидации",
              details: [],
            },
          },
          { status: 422 },
        ),
      ),
    );
    renderForm();
    await user.type(screen.getByLabelText("Ваше имя"), "Иван");
    await user.type(screen.getByLabelText("Телефон"), "291234567");
    await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
    expect(
      await screen.findByText(
        "Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.",
      ),
    ).toBeInTheDocument();
  });
});
