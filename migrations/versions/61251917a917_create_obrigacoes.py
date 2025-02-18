"""create obrigacoes

Revision ID: 61251917a917
Revises: 097557884e3e
Create Date: 2025-02-18 00:03:08.642344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61251917a917'
down_revision: Union[str, None] = '097557884e3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'obrigacao_acessoria',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('periodicidade', sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("obrigacao_acessoria")
