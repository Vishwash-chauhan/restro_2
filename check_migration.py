"""
Check migration status in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def check_migration_status():
    with app.app_context():
        # Get current migration version
        result = db.session.execute(text('SELECT version_num FROM alembic_version')).fetchall()
        print("Current migrations in the database:")
        for row in result:
            print(f"- {row[0]}")

if __name__ == "__main__":
    check_migration_status()
