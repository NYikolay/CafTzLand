"use client";

import { useEffect, useState } from "react";
import { NAV_LINKS } from "@/components/layout/nav-links";
import { ButtonLink } from "@/components/ui/button";

export function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOpen(false);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  return (
    <div className="lg:hidden">
      <button
        type="button"
        aria-expanded={isOpen}
        aria-controls="mobile-menu"
        aria-label={isOpen ? "Закрыть меню" : "Открыть меню"}
        onClick={() => setIsOpen((value) => !value)}
        className="flex h-10 w-10 flex-col items-center justify-center gap-[5px]"
      >
        <span className={`h-px w-6 bg-ink transition-transform ${isOpen ? "translate-y-[3px] rotate-45" : ""}`} />
        <span className={`h-px w-6 bg-ink transition-transform ${isOpen ? "-translate-y-[3px] -rotate-45" : ""}`} />
      </button>

      {isOpen ? (
        <div
          id="mobile-menu"
          className="fixed inset-x-0 top-[120px] bottom-0 z-50 flex flex-col gap-6 bg-cream px-4 py-8"
        >
          <nav aria-label="Мобильная навигация" className="flex flex-col gap-5">
            {NAV_LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className="font-serif text-3xl"
              >
                {link.label}
              </a>
            ))}
          </nav>
          <ButtonLink href="#zayavka" onClick={() => setIsOpen(false)} className="w-fit">
            Оставить заявку
            <span aria-hidden>↗</span>
          </ButtonLink>
        </div>
      ) : null}
    </div>
  );
}
