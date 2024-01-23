
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision: str = '8de65e3d4287'
down_revision: Union[str, None] = 'bf94b03a5fb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'grades',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('student_id', sa.Integer(), ForeignKey('students.id'), nullable=False),
        sa.Column('subject_id', sa.Integer(), ForeignKey('subjects.id'), nullable=False),
        sa.Column('grade', sa.Integer(), nullable=False),
        sa.Column('date_received', sa.Date(), nullable=False)
    )


def downgrade():
    op.drop_table('grades')