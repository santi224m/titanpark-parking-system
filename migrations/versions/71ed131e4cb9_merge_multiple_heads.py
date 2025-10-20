"""merge multiple heads

Revision ID: 71ed131e4cb9
Revises: 680786602cbb, 9adafa7c70e2
Create Date: 2025-10-19 20:58:55.271477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71ed131e4cb9'
down_revision: Union[str, Sequence[str], None] = ('680786602cbb', '9adafa7c70e2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
