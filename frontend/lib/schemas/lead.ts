import { z } from "zod";
import { normalizeByPhone } from "@/lib/phone";

export const INTEREST_VALUES = ["subscription", "one_time", "question"] as const;

export const leadFormSchema = z.object({
  interest: z.enum(INTEREST_VALUES),
  name: z
    .string()
    .trim()
    .min(1, "Напишите, как к вам обращаться")
    .max(200, "Слишком длинное имя"),
  phone_number: z
    .string()
    .min(1, "Введите номер телефона")
    .refine(
      (value) => normalizeByPhone(value) !== null,
      "Пожалуйста, введите корректный номер телефона",
    ),
  comment: z.string().max(2000, "Комментарий слишком длинный").optional(),
  product_id: z.string().optional(),
});

export type LeadFormValues = z.input<typeof leadFormSchema>;

export const leadApiSchema = z.object({
  name: z.string().trim().min(1).max(200),
  phone_number: z.string().min(1).max(32),
  interest: z.enum(INTEREST_VALUES),
  product_id: z.number().int().positive().nullish(),
  comment: z.string().max(2000).nullish(),
  source: z.record(z.string(), z.string()).nullish(),
});

export type LeadApiPayload = z.infer<typeof leadApiSchema>;

export function toLeadApiPayload(
  values: LeadFormValues,
): Omit<LeadApiPayload, "source"> {
  const normalizedPhone = normalizeByPhone(values.phone_number ?? "");
  const comment = values.comment?.trim();
  return {
    name: values.name.trim(),
    phone_number: normalizedPhone ?? values.phone_number,
    interest: values.interest,
    product_id: values.product_id ? Number(values.product_id) : null,
    comment: comment ? comment : null,
  };
}
