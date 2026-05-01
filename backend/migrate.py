"""
Migration script: adds new columns to the existing 'interactions' table.
Safe to re-run — uses IF NOT EXISTS.
"""
import os
from dotenv import load_dotenv
load_dotenv()

import sqlalchemy as sa

DATABASE_URL = os.getenv("DATABASE_URL")
engine = sa.create_engine(DATABASE_URL)

migrations = [
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS specialty VARCHAR(100)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS interaction_type VARCHAR(50)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS product_discussed VARCHAR(255)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS outcome VARCHAR(255)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS date VARCHAR(50)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS time VARCHAR(50)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW()",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ",
]

with engine.connect() as conn:
    for sql in migrations:
        print(f"Running: {sql}")
        conn.execute(sa.text(sql))
        conn.commit()
        print("  ✓ Done")

print("\n✅ Migration complete!")
