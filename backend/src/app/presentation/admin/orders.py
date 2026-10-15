from typing import Any, ClassVar

from sqladmin import ModelView
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter, OperationColumnFilter

from app.infrastructure.db.models.order import Order


class OrderAdmin(ModelView, model=Order):
    name = "Заявка"
    name_plural = "Заявки"
    icon = "fa-solid fa-envelope"
    identity = "order"

    column_list: ClassVar[list[Any]] = [
        Order.id,
        Order.created_at,
        Order.name,
        Order.phone_number,
        Order.interest,
        Order.product_id,
        Order.utm_source,
        Order.utm_content,
        Order.page_url,
        Order.is_handled,
    ]
    column_searchable_list: ClassVar[list[Any]] = [Order.name, Order.phone_number]
    column_sortable_list: ClassVar[list[Any]] = [Order.created_at, Order.is_handled]
    column_default_sort: ClassVar[list[Any]] = [(Order.created_at, True)]
    column_filters: ClassVar[list[Any]] = [
        BooleanFilter(Order.is_handled),
        AllUniqueStringValuesFilter(Order.interest),
        AllUniqueStringValuesFilter(Order.utm_source),
        OperationColumnFilter(Order.created_at),
    ]
    form_columns: ClassVar[list[Any]] = [Order.is_handled]
    can_create = False
    can_delete = False
