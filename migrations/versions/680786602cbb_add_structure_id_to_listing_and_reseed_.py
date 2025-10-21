from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "680786602cbb"         # keep your file's revision id
down_revision = "1d313a52aefd"    # the previous migration id
branch_labels = None
depends_on = None

def _has_column(inspector, table_name, column_name):
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))

def _has_fk(inspector, table_name, constraint_name):
    return any(fk.get("name") == constraint_name for fk in inspector.get_foreign_keys(table_name))

def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # 1) Add structure_id if missing
    if not _has_column(inspector, "listing", "structure_id"):
        op.add_column("listing", sa.Column("structure_id", sa.Integer(), nullable=True))

    # 2) Drop any incorrect FK on price (if it exists)
    if _has_fk(inspector, "listing", "listing_price_fkey"):
        op.drop_constraint("listing_price_fkey", "listing", type_="foreignkey")

    # 3) Seed parking_structure ONLY if empty, and ensure the order your tests expect
    count = bind.execute(sa.text("SELECT COUNT(*) FROM parking_structure")).scalar()
    if count == 0:
        bind.execute(sa.text("TRUNCATE TABLE parking_structure RESTART IDENTITY;"))
        bind.execute(sa.text("""
            INSERT INTO parking_structure (name) VALUES
            ('Nutwood Structure'),
            ('State College Structure'),
            ('Eastside North'),
            ('Eastside South');
        """))

    # 4) Backfill structure_id to a sane default (defensive; usually no rows in CI)
    bind.execute(sa.text("""
        UPDATE listing
        SET structure_id = 1
        WHERE structure_id IS NULL;
    """))

    # 5) Make structure_id NOT NULL + add proper FK (guard if it already exists)
    #    If the column was just added, it’s currently nullable == True; this will enforce it.
    op.alter_column("listing", "structure_id", nullable=False)

    if not _has_fk(inspector, "listing", "listing_structure_id_fkey"):
        op.create_foreign_key(
            "listing_structure_id_fkey",
            "listing",
            "parking_structure",
            ["structure_id"],
            ["id"],
            ondelete="RESTRICT",
        )

def downgrade():
    # Drop FK if present
    if_exists = True
    try:
        op.drop_constraint("listing_structure_id_fkey", "listing", type_="foreignkey")
    except Exception:
        pass
    # Drop column if present
    try:
        op.drop_column("listing", "structure_id")
    except Exception:
        pass