import { Suspense } from "react";
import { LeadFormProvider } from "@/components/form/lead-form-context";
import { SiteHeader } from "@/components/layout/site-header";
import { CoffeeCatalog } from "@/components/sections/coffee-catalog";
import { DeliverySection } from "@/components/sections/delivery-section";
import { HeroSection } from "@/components/sections/hero-section";
import { LeadSection } from "@/components/sections/lead-section";
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
        <DeliverySection />
        <LeadSection />
      </main>
    </LeadFormProvider>
  );
}
