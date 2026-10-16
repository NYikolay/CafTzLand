"use client";

import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { Field } from "@/components/form/field";
import { useLeadForm } from "@/components/form/lead-form-context";
import { RadioCard } from "@/components/form/radio-card";
import { Button } from "@/components/ui/button";
import { ArrowUpRightIcon } from "@/components/ui/icons";
import { RoastMark } from "@/components/ui/roast-mark";
import { interpretLeadResponse, GENERIC_LEAD_ERROR } from "@/lib/api/lead";
import { collectLeadSource } from "@/lib/lead-source";
import { BY_PHONE_MASK, formatByPhone } from "@/lib/phone";
import { leadFormSchema, toLeadApiPayload, type LeadFormValues } from "@/lib/schemas/lead";
import type { InterestOption, Product } from "@/lib/types";

type LeadFormProps = {
  products: Product[];
  options: InterestOption[];
};

export function LeadForm({ products, options }: LeadFormProps) {
  const { selectedInterest, selectedProductId } = useLeadForm();

  const {
    register,
    handleSubmit,
    setValue,
    setError,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<LeadFormValues>({
    resolver: zodResolver(leadFormSchema),
    defaultValues: {
      interest: "subscription",
      name: "",
      phone_number: "",
      comment: "",
      product_id: "",
    },
  });

  useEffect(() => {
    if (selectedInterest) {
      setValue("interest", selectedInterest, { shouldValidate: true });
    }
  }, [selectedInterest, setValue]);

  useEffect(() => {
    if (selectedProductId !== null) {
      setValue("product_id", String(selectedProductId), { shouldValidate: true });
    }
  }, [selectedProductId, setValue]);

  const onSubmit = handleSubmit(async (values) => {
    try {
      const response = await fetch("/api/v1/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...toLeadApiPayload(values),
          source: collectLeadSource(),
        }),
      });
      const body = await response.json().catch(() => null);
      const interpreted = interpretLeadResponse(response.status, body);

      if (interpreted.status === "validation") {
        const fieldErrors = Object.entries(interpreted.fieldErrors);
        if (fieldErrors.length > 0) {
          for (const [field, message] of fieldErrors) {
            setError(field as keyof LeadFormValues, { message });
          }
        } else {
          toast.error(interpreted.message ?? GENERIC_LEAD_ERROR);
        }
        return;
      }

      if (interpreted.status === "created") {
        toast.success("Спасибо! Заявка отправлена — менеджер Вам перезвонит");
        reset();
        return;
      }

      if (interpreted.status === "duplicate") {
        toast.success("Ваша зявка уже была получена, пожалуйста, ожидайте - менеджер Вам перезвонит");
        reset();
        return;
      }

      toast.error(interpreted.message);
    } catch {
      toast.error(GENERIC_LEAD_ERROR);
    }
  });

  return (
    <form onSubmit={onSubmit} noValidate className="rounded-md bg-cream p-6 md:p-9">
      <div className="mb-6 flex items-start justify-between">
        <h3 className="font-serif text-[34px] leading-tight tracking-[-1px]">Начнём с заявки</h3>
        <RoastMark width={35} height={39} />
      </div>

      <fieldset className="mb-6">
        <legend className="mb-3 text-sm">Как хотите заказывать?</legend>
        <div className="grid grid-cols-2 gap-2 lg:grid-cols-3">
          {options.map((option) => (
            <RadioCard
              key={option.value}
              label={option.label}
              value={option.value}
              {...register("interest")}
            />
          ))}
        </div>
        {errors.interest ? (
          <p role="alert" className="mt-2 text-[13px] leading-snug text-accent-deep">
            {errors.interest.message}
          </p>
        ) : null}
      </fieldset>

      <div className="grid gap-5">
        <Field id="lead-name" label="Ваше имя *" error={errors.name?.message}>
          <input
            id="lead-name"
            {...register("name")}
            placeholder="Как к вам обращаться"
            aria-invalid={errors.name ? true : undefined}
            aria-describedby={errors.name ? "lead-name-error" : undefined}
            className="h-12 w-full rounded-[3px] border border-line bg-paper px-4 text-[16px] outline-none focus:border-accent"
          />
        </Field>

        <Field id="lead-phone" label="Телефон *" error={errors.phone_number?.message}>
          <input
            id="lead-phone"
            type="tel"
            inputMode="tel"
            autoComplete="tel"
            {...register("phone_number")}
            onChange={(event) =>
              setValue("phone_number", formatByPhone(event.target.value), {
                shouldValidate: false,
              })
            }
            placeholder={BY_PHONE_MASK}
            aria-invalid={errors.phone_number ? true : undefined}
            aria-describedby={errors.phone_number ? "lead-phone-error" : undefined}
            className={`h-12 w-full rounded-[3px] border bg-paper px-4 text-[16px] outline-none focus:border-accent ${
              errors.phone_number ? "border-accent" : "border-line"
            }`}
          />
        </Field>

        <Field id="lead-comment" label="Комментарий" error={errors.comment?.message}>
          <textarea
            id="lead-comment"
            rows={3}
            {...register("comment")}
            placeholder="Оставьте ваш вопрос тут"
            className="w-full rounded-[3px] border border-line bg-paper px-4 py-3 text-[16px] outline-none focus:border-accent"
          />
        </Field>

        <Field
          id="lead-coffee"
          label="Какой кофе желаете?"
          error={errors.product_id?.message}
        >
          <div className="relative w-full">
            <select
                id="lead-coffee"
                {...register("product_id")}
                className="appearance-none h-12 w-full rounded-[3px] cursor-pointer border border-line bg-paper pl-4 pr-10 text-[16px] outline-none focus:border-accent"
            >
              <option value="">Помогите выбрать</option>
              {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name}
                  </option>
              ))}
            </select>
            <svg
                className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </Field>
      </div>

      <Button type="submit" disabled={isSubmitting} className="mt-6 w-full ">
        {isSubmitting ? "Отправляем…" : "Оставить заявку"}
        <ArrowUpRightIcon />
      </Button>

      <p className="mt-4 text-[13px] leading-relaxed text-muted">
        Менеджер перезвонит, поможет выбрать кофе, уточнит доставку и оформит заказ.
      </p>
    </form>
  );
}
