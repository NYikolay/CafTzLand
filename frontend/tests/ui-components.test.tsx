import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Button, ButtonLink } from "@/components/ui/button";
import { Eyebrow } from "@/components/ui/eyebrow";

describe("Button", () => {
  it("рендерит кнопку с типом button по умолчанию", () => {
    render(<Button>Оставить заявку</Button>);
    const button = screen.getByRole("button", { name: "Оставить заявку" });
    expect(button).toHaveAttribute("type", "button");
    expect(button.className).toContain("bg-accent");
  });
});

describe("ButtonLink", () => {
  it("рендерит ссылку с вариантом outline", () => {
    render(
      <ButtonLink href="#coffee" variant="outline">
        Выбрать кофе
      </ButtonLink>,
    );
    const link = screen.getByRole("link", { name: "Выбрать кофе" });
    expect(link).toHaveAttribute("href", "#coffee");
    expect(link.className).toContain("border-ink");
  });
});

describe("Eyebrow", () => {
  it("рендерит mono-метку", () => {
    render(<Eyebrow>01 / Главная история</Eyebrow>);
    const element = screen.getByText("01 / Главная история");
    expect(element.className).toContain("font-mono");
    expect(element.className).toContain("text-accent");
  });
});
