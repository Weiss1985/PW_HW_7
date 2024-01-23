
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1abc1bb63e84'
down_revision: Union[str, None] = 'f5030de08cdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'])
        )


def downgrade() -> None:
    op.drop_table('students')
