export type ProductKind = "beans" | "assorted" | "set";

export type ProductVariant = {
  id: number;
  packaging_label: string;
  price: string;
  weight_grams: number | null;
  units: number | null;
};

export type Product = {
  id: number;
  code: string;
  name: string;
  kind: ProductKind;
  tasting_notes: string | null;
  description: string | null;
  brew_method: string | null;
  variants: ProductVariant[];
};

export type LeadInterest = "subscription" | "one_time" | "question";

export type LeadPayload = {
  name: string;
  phone_number: string;
  interest: LeadInterest;
  product_id?: number | null;
  comment?: string | null;
  source?: Record<string, string> | null;
};

export type LeadFieldErrors = Partial<
  Record<"name" | "phone_number" | "interest" | "product_id" | "comment", string>
>;

export type LeadResult =
  | { status: "created"; id: number }
  | { status: "duplicate"; id: number }
  | { status: "validation"; fieldErrors: LeadFieldErrors }
  | { status: "error"; message: string };

export type InterestOption = {
  value: LeadInterest;
  label: string;
};
