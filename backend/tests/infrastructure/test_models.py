from typing import cast

from sqlalchemy import CheckConstraint, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from app.infrastructure.db.models import Order, Product, ProductVariant, TelegramSubscriber


def test_table_names() -> None:
    assert cast(Table, Product.__table__).name == "products"
    assert cast(Table, ProductVariant.__table__).name == "product_variants"
    assert cast(Table, Order.__table__).name == "orders"


def test_order_indexes() -> None:
    names = {index.name for index in cast(Table, Order.__table__).indexes}
    assert names == {"ix_orders_phone_number_created_at", "ix_orders_created_at"}


def test_variant_unique_constraint() -> None:
    names = {constraint.name for constraint in cast(Table, ProductVariant.__table__).constraints}
    assert "uq_product_variants_product_id" in names


def test_order_check_constraints() -> None:
    names = {constraint.name for constraint in cast(Table, Order.__table__).constraints}
    assert "ck_orders_interest_allowed" in names


def test_order_interest_constraint_allows_russian_names() -> None:
    table = cast(Table, Order.__table__)
    constraint = cast(
        CheckConstraint,
        next(
            constraint
            for constraint in table.constraints
            if constraint.name == "ck_orders_interest_allowed"
        ),
    )
    sql = str(constraint.sqltext)

    assert "'Подписка'" in sql
    assert "'Разовый заказ'" in sql
    assert "'Вопрос'" in sql


def test_order_interest_column_width() -> None:
    column_type = cast(Table, Order.__table__).c.interest.type

    assert isinstance(column_type, String)
    assert column_type.length == 30


def test_source_extra_is_jsonb() -> None:
    assert isinstance(Order.__table__.c.source_extra.type, JSONB)


def test_order_product_fk_sets_null() -> None:
    fk = next(iter(Order.__table__.c.product_id.foreign_keys))
    assert fk.ondelete == "SET NULL"


def test_telegram_subscriber_table_name() -> None:
    assert cast(Table, TelegramSubscriber.__table__).name == "telegram_subscribers"


def test_telegram_subscriber_unique_user_id() -> None:
    names = {
        constraint.name for constraint in cast(Table, TelegramSubscriber.__table__).constraints
    }
    assert "uq_telegram_subscribers_telegram_user_id" in names


def test_telegram_subscriber_active_has_server_default() -> None:
    assert TelegramSubscriber.__table__.c.is_active.server_default is not None
