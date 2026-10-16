import type { Product } from "@/lib/types";

export const fixtureProducts: Product[] = [
  {
    id: 1,
    code: "BR",
    name: "Бразилия Серрадо",
    kind: "beans",
    tasting_notes: "Шоколад · орех · карамель",
    description: "Плотный и спокойный. Понятный кофе на каждый день.",
    brew_method: "Для эспрессо, турки и молочных напитков",
    variants: [
      { id: 1, packaging_label: "250 Г", price: "26.00", weight_grams: 250, units: null },
      { id: 2, packaging_label: "500 Г", price: "52.00", weight_grams: 500, units: null },
    ],
  },
  {
    id: 2,
    code: "CO",
    name: "Колумбия Уила",
    kind: "beans",
    tasting_notes: "Красное яблоко · какао · тростниковый сахар",
    description: "Сочный, но без резкости. Когда хочется чуть ярче.",
    brew_method: "Для фильтра и эспрессо",
    variants: [
      { id: 3, packaging_label: "250 Г", price: "29.00", weight_grams: 250, units: null },
      { id: 4, packaging_label: "500 Г", price: "58.00", weight_grams: 500, units: null },
    ],
  },
  {
    id: 3,
    code: "ET",
    name: "Эфиопия Иргачеффе",
    kind: "beans",
    tasting_notes: "Бергамот · цитрус · цветочный мёд",
    description: "Лёгкий и ароматный. Хорош без молока.",
    brew_method: "Для воронки, фильтра и аэропресса",
    variants: [
      { id: 5, packaging_label: "250 Г", price: "32.00", weight_grams: 250, units: null },
      { id: 6, packaging_label: "500 Г", price: "64.00", weight_grams: 500, units: null },
    ],
  },
  {
    id: 4,
    code: "DR",
    name: "Дрип-пакеты «Кварта» (Ассорти)",
    kind: "assorted",
    tasting_notes: "Кофе в дорогу · для офиса",
    description:
      "10 порционных пакетиков. Внутри — Бразилия, Колумбия и Эфиопия. Идеально для офиса и поездок. Просто добавь горячую воду.",
    brew_method: null,
    variants: [
      { id: 7, packaging_label: "10 шт", price: "18.00", weight_grams: null, units: 10 },
      { id: 8, packaging_label: "20 шт", price: "36.00", weight_grams: null, units: 20 },
    ],
  },
  {
    id: 5,
    code: "SET",
    name: "Набор Кварты",
    kind: "set",
    tasting_notes: "2 × 250 г каждую неделю",
    description: "Свежая обжарка для дома или офиса. Менеджер поможет собрать набор.",
    brew_method: null,
    variants: [
      { id: 9, packaging_label: "2 × 250 г", price: "48.00", weight_grams: 500, units: null },
    ],
  },
];
