import Link from "next/link";
import { MobileMenu } from "@/components/layout/mobile-menu";
import { NAV_LINKS } from "@/components/layout/nav-links";
import { ButtonLink } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import { RoastMark } from "@/components/ui/roast-mark";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-line bg-cream">
      <div className="flex items-center justify-between border-b border-line px-4 py-2 font-mono text-[10px] uppercase tracking-[1px] text-muted lg:hidden">
        <span>Кофейная мастерская</span>
        <span>Минск · С 2019 года</span>
      </div>
      <Container>
        <div className="flex h-[72px] items-center justify-between lg:h-[92px]">
          <Link href="/" className="flex items-center gap-4" aria-label="Кварта — на главную">
            <RoastMark />
            <span className="flex flex-col">
              <span className="font-serif text-[22px] leading-none">Кварта</span>
              <span className="mt-1 hidden font-mono text-[10px] uppercase leading-tight tracking-[1px] text-muted lg:block">
                Кофейная мастерская
                <br />
                Минск · С 2019 года
              </span>
            </span>
          </Link>

          <nav aria-label="Основная навигация" className="hidden items-center gap-6 lg:flex">
            {NAV_LINKS.map((link) => (
              <a key={link.href} href={link.href} className="text-sm text-ink hover:text-accent">
                {link.label}
              </a>
            ))}
            <ButtonLink href="#zayavka">
              Оставить заявку
              <span aria-hidden>↗</span>
            </ButtonLink>
          </nav>

          <MobileMenu />
        </div>
      </Container>
    </header>
  );
}
