import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { toast } from "sonner";
import { LeadForm } from "@/components/form/lead-form";
import { LeadFormProvider, useLeadForm } from "@/components/form/lead-form-context";
import { SubscribeCtaButton } from "@/components/form/subscribe-cta-button";
import { fixtureLeadOptions } from "@/lib/fixtures/lead-options";
import { fixtureProducts } from "@/lib/fixtures/products";

vi.mock("sonner", () => ({
  toast: { success: vi.fn(), error: vi.fn() },
}));

const GENERIC_LEAD_ERROR_TEXT =
  "Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.";

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

async function fillAndSubmit(
  user: ReturnType<typeof userEvent.setup>,
  phone = "291234567",
) {
  await user.type(screen.getByLabelText("Ваше имя"), "Иван");
  await user.type(screen.getByLabelText("Телефон"), phone);
  await user.click(screen.getByRole("button", { name: /Оставить заявку/ }));
}

describe("LeadForm", () => {
  afterEach(() => {
    vi.clearAllMocks();
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

  it("показывает текст ошибки телефона из макета и не показывает тост", async () => {
    const user = userEvent.setup();
    renderForm();
    await fillAndSubmit(user, "123");
    expect(
      await screen.findByText("Пожалуйста, введите корректный номер телефона"),
    ).toBeInTheDocument();
    expect(toast.error).not.toHaveBeenCalled();
  });

  it("показывает тост успеха и очищает форму при 201", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({ id: 1, duplicate: false }, { status: 201 }),
      ),
    );
    renderForm();
    await fillAndSubmit(user);
    await waitFor(() =>
      expect(toast.success).toHaveBeenCalledWith(
        "Спасибо! Заявка отправлена — менеджер перезвонит.",
      ),
    );
    expect(screen.getByLabelText("Ваше имя")).toHaveValue("");
    expect(screen.getByLabelText("Телефон")).toHaveValue("");
  });

  it("показывает успешный тост при дубле и очищает форму", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({ id: 1, duplicate: true }, { status: 200 }),
      ),
    );
    renderForm();
    await fillAndSubmit(user);
    await waitFor(() =>
      expect(toast.success).toHaveBeenCalledWith(
        "Заявка уже отправлена — менеджер перезвонит.",
      ),
    );
    expect(screen.getByLabelText("Ваше имя")).toHaveValue("");
    expect(toast.error).not.toHaveBeenCalled();
  });

  it("показывает msg от backend из 422 под полем без тоста", async () => {
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
    await fillAndSubmit(user, "375291234567");
    expect(await screen.findByText("Номер не обслуживается")).toBeInTheDocument();
    expect(toast.error).not.toHaveBeenCalled();
  });

  it("показывает сообщение backend при 422 без деталей", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json(
          {
            error: {
              code: "validation_error",
              message:
                "Выбранный кофе больше недоступен — выберите другой или оставьте поле пустым",
            },
          },
          { status: 422 },
        ),
      ),
    );
    renderForm();
    await fillAndSubmit(user);
    await waitFor(() =>
      expect(toast.error).toHaveBeenCalledWith(
        "Выбранный кофе больше недоступен — выберите другой или оставьте поле пустым",
      ),
    );
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
    await fillAndSubmit(user);
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
    await fillAndSubmit(user);
    expect(await screen.findByText("Подписка недоступна")).toBeInTheDocument();
  });

  it("показывает общий тост при 500", async () => {
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
    await fillAndSubmit(user);
    await waitFor(() =>
      expect(toast.error).toHaveBeenCalledWith(GENERIC_LEAD_ERROR_TEXT),
    );
  });
});
