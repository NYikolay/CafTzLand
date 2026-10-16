import { ImageResponse } from "next/og";

export const alt = "Кварта — свежая обжарка кофе каждый четверг, Минск";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          backgroundColor: "#f4f0e7",
          color: "#30251f",
          padding: 80,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
          <div
            style={{
              width: 70,
              height: 78,
              backgroundColor: "#c8472c",
              color: "#fffcf5",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 34,
              fontWeight: 500,
            }}
          >
            КВ
          </div>
          <div style={{ fontSize: 40 }}>Кварта — кофейная мастерская</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ fontSize: 64, lineHeight: 1.1 }}>Свежая обжарка каждый четверг</div>
          <div style={{ fontSize: 32, color: "#75695f" }}>
            Развоз по пятницам · Минск, ул. Короля, 9
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
