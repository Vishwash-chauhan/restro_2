"""
Examine the category table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def examine_categories():
    with app.app_context():
        # Get restaurant ID
        restaurant_id = db.session.execute(text('SELECT id FROM restaurant WHERE slug = "shiv-dhaba"')).fetchone()[0]
        print(f"Restaurant ID for Shiv Dhaba: {restaurant_id}")
        
        # Get category table structure
        result = db.session.execute(text("DESCRIBE category")).fetchall()
        print("\nCategory table structure:")
        for row in result:
            print(f"{row[0]} | {row[1]} | Nullable: {row[2]} | Key: {row[3]} | Default: {row[4]} | Extra: {row[5]}")
        
        # Get category records
        result = db.session.execute(text("SELECT * FROM category")).fetchall()
        print("\nCategory records:")
        for idx, row in enumerate(result):
            print(f"Row {idx+1}: {row}")
            
        # Try direct update with proper SQL syntax
        print("\nAttempting to update category records...")
        try:
            db.session.execute(text(f"UPDATE category SET restaurant_id = {restaurant_id}"))
            db.session.commit()
            print("Update successful")
            
            # Verify update
            count = db.session.execute(text(f"SELECT COUNT(*) FROM category WHERE restaurant_id = {restaurant_id}")).fetchone()[0]
            print(f"Categories now linked to restaurant: {count}")
        except Exception as e:
            print(f"Update failed: {str(e)}")

if __name__ == "__main__":
    examine_categories()
