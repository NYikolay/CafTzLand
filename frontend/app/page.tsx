import { LeadFormProvider } from "@/components/form/lead-form-context";
import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";
import { HeroSection } from "@/components/sections/hero-section";
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
      </main>
      <SiteFooter />
    </LeadFormProvider>
  );
}
