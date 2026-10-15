"""interest russian names

Revision ID: c3f1a2b4d5e6
Revises: b2e1d3c45a67
Create Date: 2026-10-15 23:30:00.000000+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c3f1a2b4d5e6'
down_revision: Union[str, Sequence[str], None] = 'b2e1d3c45a67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('ck_orders_interest_allowed'), 'orders', type_='check')
    op.execute(
        "UPDATE orders SET interest = CASE interest "
        "WHEN 'subscription' THEN 'Подписка' "
        "WHEN 'one_time' THEN 'Разовый заказ' "
        "WHEN 'question' THEN 'Вопрос' "
        "ELSE interest END"
    )
    op.alter_column(
        'orders',
        'interest',
        existing_type=sa.String(length=20),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.create_check_constraint(
        op.f('ck_orders_interest_allowed'),
        'orders',
        "interest IN ('Подписка', 'Разовый заказ', 'Вопрос')",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('ck_orders_interest_allowed'), 'orders', type_='check')
    op.execute(
        "UPDATE orders SET interest = CASE interest "
        "WHEN 'Подписка' THEN 'subscription' "
        "WHEN 'Разовый заказ' THEN 'one_time' "
        "WHEN 'Вопрос' THEN 'question' "
        "ELSE interest END"
    )
    op.alter_column(
        'orders',
        'interest',
        existing_type=sa.String(length=30),
        type_=sa.String(length=20),
        existing_nullable=False,
    )
    op.create_check_constraint(
        op.f('ck_orders_interest_allowed'),
        'orders',
        "interest IN ('subscription', 'one_time', 'question')",
    )
