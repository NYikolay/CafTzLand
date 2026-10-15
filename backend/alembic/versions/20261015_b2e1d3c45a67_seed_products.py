"""seed products

Revision ID: b2e1d3c45a67
Revises: a1f0c2d34b56
Create Date: 2026-10-15 19:05:00.000000+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b2e1d3c45a67'
down_revision: Union[str, Sequence[str], None] = 'a1f0c2d34b56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PRODUCTS = [
    {
        'id': 1,
        'code': 'BR',
        'name': 'Бразилия Серрадо',
        'kind': 'beans',
        'tasting_notes': 'Шоколад · орех · карамель',
        'description': 'Плотный и спокойный. Понятный кофе на каждый день.',
        'brew_method': 'Для эспрессо, турки и молочных напитков',
        'is_active': True,
        'sort_order': 1,
    },
    {
        'id': 2,
        'code': 'CO',
        'name': 'Колумбия Уила',
        'kind': 'beans',
        'tasting_notes': 'Красное яблоко · какао · тростниковый сахар',
        'description': 'Сочный, но без резкости. Когда хочется чуть ярче.',
        'brew_method': 'Для фильтра и эспрессо',
        'is_active': True,
        'sort_order': 2,
    },
    {
        'id': 3,
        'code': 'ET',
        'name': 'Эфиопия Иргачеффе',
        'kind': 'beans',
        'tasting_notes': 'Бергамот · цитрус · цветочный мёд',
        'description': 'Лёгкий и ароматный. Хорош без молока.',
        'brew_method': 'Для воронки, фильтра и аэропресса',
        'is_active': True,
        'sort_order': 3,
    },
    {
        'id': 4,
        'code': 'DR',
        'name': 'Дрип-пакеты «Кварта» (Ассорти)',
        'kind': 'assorted',
        'tasting_notes': 'Кофе в дорогу · для офиса',
        'description': (
            '10 порционных пакетиков. Внутри — Бразилия, Колумбия и Эфиопия. '
            'Идеально для офиса и поездок. Просто добавь горячую воду.'
        ),
        'brew_method': None,
        'is_active': True,
        'sort_order': 4,
    },
    {
        'id': 5,
        'code': 'SET',
        'name': 'Набор Кварты',
        'kind': 'set',
        'tasting_notes': '2 × 250 г каждую неделю',
        'description': (
            'Набор кофейной подписки: 2 × 250 г свежей обжарки каждую неделю. '
            'Стоимость доставки уточнит менеджер при звонке.'
        ),
        'brew_method': None,
        'is_active': True,
        'sort_order': 5,
    },
]

VARIANTS = [
    {
        'id': 1,
        'product_id': 1,
        'packaging_label': '250 Г',
        'price': '26.00',
        'weight_grams': 250,
        'units': None,
        'is_active': True,
        'sort_order': 1,
    },
    {
        'id': 2,
        'product_id': 1,
        'packaging_label': '500 Г',
        'price': '52.00',
        'weight_grams': 500,
        'units': None,
        'is_active': True,
        'sort_order': 2,
    },
    {
        'id': 3,
        'product_id': 2,
        'packaging_label': '250 Г',
        'price': '29.00',
        'weight_grams': 250,
        'units': None,
        'is_active': True,
        'sort_order': 1,
    },
    {
        'id': 4,
        'product_id': 2,
        'packaging_label': '500 Г',
        'price': '58.00',
        'weight_grams': 500,
        'units': None,
        'is_active': True,
        'sort_order': 2,
    },
    {
        'id': 5,
        'product_id': 3,
        'packaging_label': '250 Г',
        'price': '32.00',
        'weight_grams': 250,
        'units': None,
        'is_active': True,
        'sort_order': 1,
    },
    {
        'id': 6,
        'product_id': 3,
        'packaging_label': '500 Г',
        'price': '64.00',
        'weight_grams': 500,
        'units': None,
        'is_active': True,
        'sort_order': 2,
    },
    {
        'id': 7,
        'product_id': 4,
        'packaging_label': '10 шт',
        'price': '18.00',
        'weight_grams': None,
        'units': 10,
        'is_active': True,
        'sort_order': 1,
    },
    {
        'id': 8,
        'product_id': 4,
        'packaging_label': '20 шт',
        'price': '36.00',
        'weight_grams': None,
        'units': 20,
        'is_active': True,
        'sort_order': 2,
    },
    {
        'id': 9,
        'product_id': 5,
        'packaging_label': '2 × 250 г',
        'price': '48.00',
        'weight_grams': 500,
        'units': None,
        'is_active': True,
        'sort_order': 1,
    },
]

products_table = sa.table(
    'products',
    sa.column('id', sa.BigInteger),
    sa.column('code', sa.String),
    sa.column('name', sa.String),
    sa.column('kind', sa.String),
    sa.column('tasting_notes', sa.String),
    sa.column('description', sa.Text),
    sa.column('brew_method', sa.String),
    sa.column('is_active', sa.Boolean),
    sa.column('sort_order', sa.Integer),
)

variants_table = sa.table(
    'product_variants',
    sa.column('id', sa.BigInteger),
    sa.column('product_id', sa.BigInteger),
    sa.column('packaging_label', sa.String),
    sa.column('price', sa.Numeric),
    sa.column('weight_grams', sa.Integer),
    sa.column('units', sa.Integer),
    sa.column('is_active', sa.Boolean),
    sa.column('sort_order', sa.Integer),
)


def upgrade() -> None:
    """Upgrade data."""
    op.bulk_insert(products_table, PRODUCTS)
    op.bulk_insert(variants_table, VARIANTS)
    op.execute(
        sa.text(
            "SELECT setval(pg_get_serial_sequence('products', 'id'), "
            "(SELECT max(id) FROM products))"
        )
    )
    op.execute(
        sa.text(
            "SELECT setval(pg_get_serial_sequence('product_variants', 'id'), "
            "(SELECT max(id) FROM product_variants))"
        )
    )


def downgrade() -> None:
    """Downgrade data."""
    op.execute(sa.text("DELETE FROM products WHERE code IN ('BR', 'CO', 'ET', 'DR', 'SET')"))
