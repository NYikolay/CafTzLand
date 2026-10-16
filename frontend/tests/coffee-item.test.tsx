import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { LeadFormProvider } from "@/components/form/lead-form-context";
import { CoffeeItem } from "@/components/sections/coffee-item";
import { fixtureProducts } from "@/lib/fixtures/products";

function renderItem() {
  return render(
    <LeadFormProvider>
      <CoffeeItem product={fixtureProducts[0]} />
    </LeadFormProvider>,
  );
}

describe("CoffeeItem", () => {
  it("рендерит бейдж с видом, кодом и акцентной линией", () => {
    const { container } = renderItem();
    expect(screen.getByText(/зерно/i)).toBeInTheDocument();
    const code = screen.getByText("BR");
    expect(code.className).toContain("font-mono");
    expect(code.className).toContain("text-[25px]");
    expect(container.querySelector("span.bg-accent")).not.toBeNull();
  });

  it("держит кнопку «Хочу этот кофе» под ценами в колонке", () => {
    renderItem();
    const button = screen.getByRole("button", { name: "Хочу этот кофе" });
    const column = button.parentElement;
    expect(column?.className).toContain("flex-col");
    expect(column?.className).not.toContain("justify-between");
  });

  it("показывает способ приготовления на мобильном и десктопе", () => {
    renderItem();
    const brew = screen.getAllByText("Для эспрессо, турки и молочных напитков");
    expect(brew).toHaveLength(2);
    expect(brew.some((node) => node.className.includes("md:hidden"))).toBe(true);
    expect(
      brew.some(
        (node) => node.className.includes("hidden") && node.className.includes("md:block"),
      ),
    ).toBe(true);
  });

  it("показывает обе цены", () => {
    renderItem();
    expect(screen.getByText("26 BYN")).toBeInTheDocument();
    expect(screen.getByText("52 BYN")).toBeInTheDocument();
  });
});
