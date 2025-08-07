"""
Verify data migration for multi-tenant system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def verify_data_migration():
    with app.app_context():
        # Get restaurant ID
        restaurant_id = db.session.execute(text('SELECT id FROM restaurant WHERE slug = "shiv-dhaba"')).fetchone()[0]
        print(f"Restaurant ID for Shiv Dhaba: {restaurant_id}")
        
        # Check categories
        category_count = db.session.execute(text(f'SELECT COUNT(*) FROM category WHERE restaurant_id = {restaurant_id}')).fetchone()[0]
        total_category_count = db.session.execute(text('SELECT COUNT(*) FROM category')).fetchone()[0]
        print(f"Categories linked to restaurant: {category_count} of {total_category_count} total")
        
        # Check dishes
        dish_count = db.session.execute(text(f'SELECT COUNT(*) FROM dish WHERE restaurant_id = {restaurant_id}')).fetchone()[0]
        total_dish_count = db.session.execute(text('SELECT COUNT(*) FROM dish')).fetchone()[0]
        print(f"Dishes linked to restaurant: {dish_count} of {total_dish_count} total")
        
        # Check orders
        order_count = db.session.execute(text(f'SELECT COUNT(*) FROM shivdhaba_order WHERE restaurant_id = {restaurant_id}')).fetchone()[0]
        total_order_count = db.session.execute(text('SELECT COUNT(*) FROM shivdhaba_order')).fetchone()[0]
        print(f"Orders linked to restaurant: {order_count} of {total_order_count} total")
        
        # Check for any unlinked records
        if total_category_count > category_count:
            print("\nWARNING: Some categories are not linked to a restaurant!")
            
        if total_dish_count > dish_count:
            print("WARNING: Some dishes are not linked to a restaurant!")
            
        if total_order_count > order_count:
            print("WARNING: Some orders are not linked to a restaurant!")
            
        if total_category_count == category_count and total_dish_count == dish_count and total_order_count == order_count:
            print("\nSuccess! All records are properly linked to the restaurant.")

if __name__ == "__main__":
    verify_data_migration()
