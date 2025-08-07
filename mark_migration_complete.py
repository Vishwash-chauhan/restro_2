"""
Fix migration state in database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def fix_migration_state():
    with app.app_context():
        # Clear all existing migration records
        db.session.execute(text('DELETE FROM alembic_version'))
        db.session.commit()
        print("Cleared existing migration records")
        
        # Set the latest migration version
        db.session.execute(text('INSERT INTO alembic_version (version_num) VALUES ("53acbd2d0f4f")'))
        db.session.commit()
        print("Set migration version to 53acbd2d0f4f (latest)")
        
        print("Migration state has been fixed")

if __name__ == "__main__":
    fix_migration_state()
