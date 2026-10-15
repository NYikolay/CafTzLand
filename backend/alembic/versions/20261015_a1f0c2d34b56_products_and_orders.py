"""products and orders

Revision ID: a1f0c2d34b56
Revises: 4d28216bc024
Create Date: 2026-10-15 19:00:00.000000+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1f0c2d34b56'
down_revision: Union[str, Sequence[str], None] = '4d28216bc024'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'products',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('code', sa.String(length=8), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('kind', sa.String(length=20), nullable=False),
        sa.Column('tasting_notes', sa.String(length=300), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('brew_method', sa.String(length=300), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('sort_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kind IN ('beans', 'assorted', 'set')", name=op.f('ck_products_kind_allowed')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_products')),
        sa.UniqueConstraint('code', name=op.f('uq_products_code')),
    )
    op.create_table(
        'product_variants',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('product_id', sa.BigInteger(), nullable=False),
        sa.Column('packaging_label', sa.String(length=50), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('weight_grams', sa.Integer(), nullable=True),
        sa.Column('units', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('sort_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint('price >= 0', name=op.f('ck_product_variants_price_non_negative')),
        sa.CheckConstraint(
            'weight_grams IS NULL OR weight_grams >= 0',
            name=op.f('ck_product_variants_weight_non_negative'),
        ),
        sa.CheckConstraint(
            'units IS NULL OR units >= 0', name=op.f('ck_product_variants_units_non_negative')
        ),
        sa.ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            name=op.f('fk_product_variants_product_id_products'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_product_variants')),
        sa.UniqueConstraint(
            'product_id', 'packaging_label', name=op.f('uq_product_variants_product_id')
        ),
    )
    op.create_table(
        'orders',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('interest', sa.String(length=20), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=False),
        sa.Column('product_id', sa.BigInteger(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('is_handled', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('utm_source', sa.String(length=255), nullable=True),
        sa.Column('utm_medium', sa.String(length=255), nullable=True),
        sa.Column('utm_campaign', sa.String(length=255), nullable=True),
        sa.Column('utm_content', sa.String(length=255), nullable=True),
        sa.Column('utm_term', sa.String(length=255), nullable=True),
        sa.Column('referrer', sa.String(length=1024), nullable=True),
        sa.Column('page_url', sa.String(length=1024), nullable=True),
        sa.Column('source_extra', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint(
            "interest IN ('subscription', 'one_time', 'question')",
            name=op.f('ck_orders_interest_allowed'),
        ),
        sa.ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            name=op.f('fk_orders_product_id_products'),
            ondelete='SET NULL',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_orders')),
    )
    op.create_index('ix_orders_created_at', 'orders', ['created_at'], unique=False)
    op.create_index(
        'ix_orders_phone_number_created_at',
        'orders',
        ['phone_number', 'created_at'],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_orders_phone_number_created_at', table_name='orders')
    op.drop_index('ix_orders_created_at', table_name='orders')
    op.drop_table('orders')
    op.drop_table('product_variants')
    op.drop_table('products')
