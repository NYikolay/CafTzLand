from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

from domain.leads import INTEREST_NAMES, Lead
from domain.products import Product

MINSK_TZ = ZoneInfo("Europe/Minsk")
HEADER = "☕️ <b>Новая заявка · VitaiWorld</b>"


def render_lead_notification(lead: Lead, product: Product | None, sent_at: datetime) -> str:
    lines = [
        HEADER,
        "",
        f"👤 <b>{escape(lead.name)}</b>",
        f"📞 {escape(lead.phone_number)}",
        f"🎯 {escape(INTEREST_NAMES[lead.interest].value)}",
    ]
    if product is not None:
        lines.append(f"📦 {escape(product.name)}")
    if lead.comment:
        lines.append(f"💬 {escape(lead.comment)}")
    if lead.source is not None and lead.source.utm_source:
        lines.append(f"🌐 {escape(lead.source.utm_source)}")
    stamp = sent_at.astimezone(MINSK_TZ).strftime("%d.%m.%Y %H:%M")
    lines.extend(["", f"🕒 {stamp} (Минск) · заявка #{lead.id}"])
    return "\n".join(lines)
