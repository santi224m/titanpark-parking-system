"""create tables

Revision ID: 1d313a52aefd
Revises: 
Create Date: 2025-10-13 11:08:58.721464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1d313a52aefd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    op.create_table(
        "parking_structure",
        sa.Column("id", sa.Integer, primary_key=True),
        
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
