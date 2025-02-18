"""create initial migration

Revision ID: 097557884e3e
Revises: 
Create Date: 2025-02-17 23:55:09.969955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '097557884e3e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Empresa',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('cnpj', sa.String(50), nullable=False),
        sa.Column('endereco', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('telefone', sa.String(50), nullable=False),
    )


def downgrade() -> None:
    pass
