from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "9adafa7c70e2"
down_revision = "1d313a52aefd"  # update if your previous head differs
branch_labels = None
depends_on = None


def upgrade():
    # 1) Add structure_id column to listing if it doesn't exist
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='listing' AND column_name='structure_id'
      ) THEN
        ALTER TABLE listing ADD COLUMN structure_id INTEGER;
      END IF;
    END$$;
    """)

    # 2) Ensure FK from listing.structure_id -> parking_structure(id)
    op.execute("""
    DO $$
    DECLARE
      fk_exists INTEGER;
    BEGIN
      SELECT COUNT(*)
      INTO fk_exists
      FROM information_schema.table_constraints tc
      JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
      WHERE tc.table_name='listing'
        AND tc.constraint_type='FOREIGN KEY'
        AND kcu.column_name='structure_id';

      IF fk_exists = 0 THEN
        ALTER TABLE listing
          ADD CONSTRAINT listing_structure_id_fkey
          FOREIGN KEY (structure_id) REFERENCES parking_structure(id);
      END IF;
    END$$;
    """)

    # 3) Normalize seed rows: ensure IDs 1..4 exist and have the exact names your tests expect
    op.execute("""
    INSERT INTO parking_structure (id, name) VALUES
      (1, 'Nutwood Structure'),
      (2, 'State College Structure'),
      (3, 'Eastside North'),
      (4, 'Eastside South')
    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
    """)


def downgrade():
    # Revert names to the earlier variants (adjust if your original names differ)
    op.execute("""
    INSERT INTO parking_structure (id, name) VALUES
      (1, 'Nutwood Parking Structure'),
      (2, 'State College Parking Structure'),
      (3, 'Eastside North Parking Structure'),
      (4, 'Eastside South Parking Structure')
    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
    """)