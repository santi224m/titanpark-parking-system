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


def upgrade():

    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    op.create_table(
        "parking_structure",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column('name', sa.Text)

    )

    op.create_table(
        'vehicle',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.Text, nullable=False),
        sa.Column('make', sa.Text, nullable=False),
        sa.Column('model', sa.Text, nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
        sa.Column('color', sa.Text, nullable=False),
        sa.Column('license_plate', sa.Text, nullable=False, unique=True),
    )

    op.create_table(
        'listing',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.Text, nullable=False),
        sa.Column('post_date', sa.TIMESTAMP, server_default=sa.text('now()'), nullable=False),
        sa.Column('price', sa.Integer, sa.ForeignKey('parking_structure.id'), nullable=False),
        sa.Column('floor', sa.Integer, nullable=False),
        sa.Column('vehicle_id', sa.UUID(as_uuid=True), sa.ForeignKey('vehicle.id'), nullable=False),
        sa.Column('comment', sa.Text)
    )

    op.execute("""
               INSERT INTO parking_structure (name) VALUES
               ('Nutwood Parking Structure'),
               ('Eastside North Parking Structure'),
               ('Eastside South Parking Structure'),
               ('State College Parking Structure'),
               ('S8 Lot | Stadium Way'),
               ('S10 Lot | Associated Road'),
               ('S Lot | College Park');
               """)


def downgrade():
    op.drop_table('listing')
    op.drop_table('vehicle')
    op.drop_table('parking_structure')
