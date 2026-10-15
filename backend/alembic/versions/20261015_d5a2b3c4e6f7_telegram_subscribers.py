"""telegram subscribers

Revision ID: d5a2b3c4e6f7
Revises: c3f1a2b4d5e6
Create Date: 2026-10-15 23:35:00.000000+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd5a2b3c4e6f7'
down_revision: Union[str, Sequence[str], None] = 'c3f1a2b4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'telegram_subscribers',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('tg_link', sa.String(length=255), nullable=False),
        sa.Column('telegram_user_id', sa.BigInteger(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
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
        sa.PrimaryKeyConstraint('id', name=op.f('pk_telegram_subscribers')),
        sa.UniqueConstraint(
            'telegram_user_id', name=op.f('uq_telegram_subscribers_telegram_user_id')
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('telegram_subscribers')
