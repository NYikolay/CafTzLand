"use client";

import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { NAV_LINKS } from "@/components/layout/nav-links";
import { ButtonLink } from "@/components/ui/button";
import { ArrowUpRightIcon } from "@/components/ui/icons";

export function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const [menuTop, setMenuTop] = useState(0);
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const desktopQuery = window.matchMedia("(min-width: 1024px)");
    const onDesktopChange = (event: MediaQueryListEvent) => {
      if (event.matches) setIsOpen(false);
    };
    desktopQuery.addEventListener("change", onDesktopChange);
    return () => desktopQuery.removeEventListener("change", onDesktopChange);
  }, [isOpen]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOpen(false);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  // Прижимаем панель к нижней границе хедера.
  useLayoutEffect(() => {
    if (!isOpen) return;

    const header = rootRef.current?.closest("header");

    const update = () => {
      if (!header) return;
      setMenuTop(header.getBoundingClientRect().bottom);
    };

    update();

    const resizeObserver = header ? new ResizeObserver(update) : null;
    if (header && resizeObserver) resizeObserver.observe(header);

    window.addEventListener("resize", update);
    window.addEventListener("scroll", update, { passive: true });

    return () => {
      resizeObserver?.disconnect();
      window.removeEventListener("resize", update);
      window.removeEventListener("scroll", update);
    };
  }, [isOpen]);

  return (
      <div ref={rootRef} className="lg:hidden">
        <button
            type="button"
            aria-expanded={isOpen}
            aria-controls="mobile-menu"
            aria-label={isOpen ? "Закрыть меню" : "Открыть меню"}
            onClick={() => setIsOpen((value) => !value)}
            className="relative z-50 flex h-10 w-10 flex-col items-center justify-center gap-[5px]"
        >
        <span
            className={`h-px w-6 bg-ink transition-transform ${
                isOpen ? "translate-y-[3px] rotate-45" : ""
            }`}
        />
          <span
              className={`h-px w-6 bg-ink transition-transform ${
                  isOpen ? "-translate-y-[3px] -rotate-45" : ""
              }`}
          />
        </button>

        {isOpen ? (
            <div
                id="mobile-menu"
                style={{ top: menuTop }}
                className="fixed inset-x-0 bottom-0 z-40 flex flex-col gap-6 overflow-y-auto overscroll-contain bg-cream px-4 py-8"
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
              <ButtonLink
                  href="#zayavka"
                  onClick={() => setIsOpen(false)}
                  className="w-fit"
              >
                Оставить заявку
                <ArrowUpRightIcon />
              </ButtonLink>
            </div>
        ) : null}
      </div>
  );
}