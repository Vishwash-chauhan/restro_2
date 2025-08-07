"""
Fix any remaining data issues in the multi-tenant migration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def fix_migration_data():
    with app.app_context():
        # Get restaurant ID
        restaurant_id = db.session.execute(text('SELECT id FROM restaurant WHERE slug = "shiv-dhaba"')).fetchone()[0]
        print(f"Restaurant ID for Shiv Dhaba: {restaurant_id}")
        
        # Fix categories with missing restaurant_id
        result = db.session.execute(text(f'UPDATE category SET restaurant_id = {restaurant_id} WHERE restaurant_id IS NULL'))
        print(f"Updated {result.rowcount} categories with missing restaurant_id")
        
        # Fix dishes with missing restaurant_id
        result = db.session.execute(text(f'UPDATE dish SET restaurant_id = {restaurant_id} WHERE restaurant_id IS NULL'))
        print(f"Updated {result.rowcount} dishes with missing restaurant_id")
        
        # Fix orders with missing restaurant_id
        result = db.session.execute(text(f'UPDATE shivdhaba_order SET restaurant_id = {restaurant_id} WHERE restaurant_id IS NULL'))
        print(f"Updated {result.rowcount} orders with missing restaurant_id")
        
        db.session.commit()
        print("Data fixes committed to database")

if __name__ == "__main__":
    fix_migration_data()
