"""
Check if all necessary tables and columns are in place for multi-tenant system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text, inspect
from sqlalchemy.engine import reflection

def check_database_schema():
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check tables
        tables = inspector.get_table_names()
        print("Tables in database:")
        for table in tables:
            print(f"- {table}")
        print()
        
        # Check Restaurant table
        print("Restaurant table columns:")
        for column in inspector.get_columns('restaurant'):
            print(f"- {column['name']} ({column['type']})")
        print()
        
        # Check foreign keys
        print("Foreign keys to Restaurant table:")
        for table in ['category', 'dish', 'shivdhaba_order']:
            fks = inspector.get_foreign_keys(table)
            for fk in fks:
                if 'restaurant' in fk['referred_table']:
                    print(f"- {table}.{fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}")
        
        # Check sample data
        print("\nSample Restaurant data:")
        result = db.session.execute(text('SELECT * FROM restaurant')).fetchall()
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")

if __name__ == "__main__":
    check_database_schema()
