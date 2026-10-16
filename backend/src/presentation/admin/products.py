from typing import Any, ClassVar

from sqladmin import ModelView
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter, ForeignKeyFilter

from infrastructure.db.models.product import Product, ProductVariant


class ProductAdmin(ModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-mug-hot"
    identity = "product"

    column_list: ClassVar[list[Any]] = [
        Product.id,
        Product.code,
        Product.name,
        Product.kind,
        Product.is_active,
        Product.sort_order,
    ]
    column_searchable_list: ClassVar[list[Any]] = [Product.name, Product.code]
    column_sortable_list: ClassVar[list[Any]] = [Product.sort_order, Product.name]
    column_default_sort: ClassVar[list[Any]] = [(Product.sort_order, False)]
    column_filters: ClassVar[list[Any]] = [
        AllUniqueStringValuesFilter(Product.kind),
        BooleanFilter(Product.is_active),
    ]
    form_columns: ClassVar[list[Any]] = [
        Product.code,
        Product.name,
        Product.kind,
        Product.tasting_notes,
        Product.description,
        Product.brew_method,
        Product.is_active,
        Product.sort_order,
    ]


class ProductVariantAdmin(ModelView, model=ProductVariant):
    name = "Фасовка"
    name_plural = "Фасовки"
    icon = "fa-solid fa-weight-hanging"
    identity = "product-variant"

    column_list: ClassVar[list[Any]] = [
        ProductVariant.id,
        ProductVariant.product_id,
        ProductVariant.packaging_label,
        ProductVariant.price,
        ProductVariant.weight_grams,
        ProductVariant.units,
        ProductVariant.is_active,
        ProductVariant.sort_order,
    ]
    column_sortable_list: ClassVar[list[Any]] = [
        ProductVariant.product_id,
        ProductVariant.sort_order,
    ]
    column_filters: ClassVar[list[Any]] = [
        ForeignKeyFilter(ProductVariant.product_id, Product.name, title="Товар"),
        BooleanFilter(ProductVariant.is_active),
    ]
