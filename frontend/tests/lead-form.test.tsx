import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LeadForm } from "@/components/form/lead-form";
import { LeadFormProvider, useLeadForm } from "@/components/form/lead-form-context";
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
});
