"use client";

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { LeadInterest } from "@/lib/types";

type LeadFormContextValue = {
  selectedInterest: LeadInterest | null;
  selectedProductId: number | null;
  selectInterest: (interest: LeadInterest) => void;
  selectCoffee: (productId: number) => void;
};

const LeadFormContext = createContext<LeadFormContextValue | null>(null);

export function LeadFormProvider({ children }: { children: ReactNode }) {
  const [selectedInterest, setSelectedInterest] = useState<LeadInterest | null>(null);
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);

  const scrollToForm = useCallback(() => {
    document.getElementById("zayavka")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, []);

  const value = useMemo<LeadFormContextValue>(
    () => ({
      selectedInterest,
      selectedProductId,
      selectInterest: (interest) => {
        setSelectedInterest(interest);
        scrollToForm();
      },
      selectCoffee: (productId) => {
        setSelectedProductId(productId);
        scrollToForm();
      },
    }),
    [selectedInterest, selectedProductId, scrollToForm],
  );

  return <LeadFormContext.Provider value={value}>{children}</LeadFormContext.Provider>;
}

export function useLeadForm(): LeadFormContextValue {
  const context = useContext(LeadFormContext);
  if (!context) {
    throw new Error("useLeadForm должен использоваться внутри LeadFormProvider");
  }
  return context;
}
