"""create parking_data_history table

Revision ID: c30d1542c902
Revises: 71ed131e4cb9
Create Date: 2025-12-13 16:26:12.326283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c30d1542c902'
down_revision: Union[str, Sequence[str], None] = '71ed131e4cb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'parking_data_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('structure_id', sa.Integer, sa.ForeignKey('parking_structure.id'), nullable=False),
        sa.Column('available', sa.Integer, nullable=False),
        sa.Column('total', sa.Integer, nullable=False),
        sa.Column('perc_full', sa.Float, nullable=True),
        sa.Column('datetime', sa.DateTime, nullable=False,
                  server_default=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('parking_data_history')
