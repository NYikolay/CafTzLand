from typing import Any, ClassVar

from sqladmin import ModelView
from sqladmin.filters import BooleanFilter

from app.infrastructure.db.models.telegram_subscriber import TelegramSubscriber


class TelegramSubscriberAdmin(ModelView, model=TelegramSubscriber):
    name = "Подписчик"
    name_plural = "Подписчики"
    icon = "fa-solid fa-paper-plane"
    identity = "telegram-subscriber"

    column_list: ClassVar[list[Any]] = [
        TelegramSubscriber.id,
        TelegramSubscriber.telegram_user_id,
        TelegramSubscriber.tg_link,
        TelegramSubscriber.is_active,
        TelegramSubscriber.created_at,
    ]
    column_searchable_list: ClassVar[list[Any]] = [TelegramSubscriber.tg_link]
    column_sortable_list: ClassVar[list[Any]] = [
        TelegramSubscriber.created_at,
        TelegramSubscriber.is_active,
    ]
    column_default_sort: ClassVar[list[Any]] = [(TelegramSubscriber.created_at, True)]
    column_filters: ClassVar[list[Any]] = [BooleanFilter(TelegramSubscriber.is_active)]
    form_columns: ClassVar[list[Any]] = [
        TelegramSubscriber.tg_link,
        TelegramSubscriber.telegram_user_id,
        TelegramSubscriber.is_active,
    ]
