"""create table teachers

Revision ID: a47dc863e8a0
Revises: 1abc1bb63e84
Create Date: 2024-01-16 13:51:11.528083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a47dc863e8a0'
down_revision: Union[str, None] = '1abc1bb63e84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('teachers')
