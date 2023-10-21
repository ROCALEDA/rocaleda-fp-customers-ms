"""Set up Customer table

Revision ID: fb3813299277
Revises: 
Create Date: 2023-10-14 21:04:10.609363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb3813299277'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #op.create_table(
    #    'customer',
    #    sa.Column('id', sa.Integer, primary_key=True),
    #    sa.Column('name', sa.String(50), nullable=False),
    #)
    pass


def downgrade() -> None:
    op.drop_table('customer')
    pass
