import type { Metadata, Viewport } from "next";
import { IBM_Plex_Serif, Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const plexSerif = IBM_Plex_Serif({
  variable: "--font-plex-serif",
  subsets: ["latin", "cyrillic"],
  weight: ["400"],
  style: ["normal", "italic"],
  display: "swap",
});

// const plexMono = IBM_Plex_Mono({
//   variable: "--font-plex-mono",
//   subsets: ["latin", "cyrillic"],
//   weight: ["400", "500"],
//   display: "swap",
// });

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin", "cyrillic"],
  display: "swap",
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://tzkvvit.site";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title:
    "Кварта — кофейная мастерская в Минске: свежая обжарка, доставка по пятницам",
  description:
    "Обжариваем кофе маленькими партиями каждый четверг и развозим по Минску в пятницу. Бразилия, Колумбия, Эфиопия и дрип-пакеты. Самовывоз: ул. Короля, 9.",
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    locale: "ru_RU",
    url: "/",
    siteName: "Кварта",
    title: "Кварта — свежая обжарка кофе каждый четверг",
    description:
      "Обжарка по четвергам, развоз по пятницам. Кофе в зёрнах и дрип-пакеты из мастерской на ул. Короля, 9 в Минске.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Кварта — свежая обжарка кофе каждый четверг",
    description: "Обжарка по четвергам, развоз по пятницам. Минск, ул. Короля, 9.",
  },
};

export const viewport: Viewport = {
  themeColor: "#30251f",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="ru"
      data-scroll-behavior="smooth"
      className={`${plexSerif.variable} ${inter.variable} h-full`}
    >
      <body className="min-h-full flex flex-col">
        {children}
        <Toaster />
      </body>
    </html>
  );
}
