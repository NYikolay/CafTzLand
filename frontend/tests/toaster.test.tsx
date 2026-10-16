import { act, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { toast } from "sonner";
import { Toaster } from "@/components/ui/toaster";

describe("Toaster", () => {
  it("показывает всплывающее уведомление", async () => {
    render(<Toaster />);
    act(() => {
      toast.success("Заявка отправлена");
    });
    expect(await screen.findByText("Заявка отправлена")).toBeInTheDocument();
  });
});
