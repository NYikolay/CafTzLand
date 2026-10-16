import { Suspense } from "react";
import { LeadFormProvider } from "@/components/form/lead-form-context";
import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";
import { CoffeeCatalog } from "@/components/sections/coffee-catalog";
import { HeroSection } from "@/components/sections/hero-section";
import { SubscriptionSection } from "@/components/sections/subscription-section";
import { WeekRoute } from "@/components/sections/week-route";
import { WorkshopSection } from "@/components/sections/workshop-section";

export default function HomePage() {
  return (
    <LeadFormProvider>
      <SiteHeader />
      <main className="flex-1">
        <HeroSection />
        <WeekRoute />
        <WorkshopSection />
        <Suspense fallback={<div className="h-[600px] bg-cream-deep" aria-hidden />}>
          <CoffeeCatalog />
        </Suspense>
        <SubscriptionSection />
      </main>
      <SiteFooter />
    </LeadFormProvider>
  );
}
