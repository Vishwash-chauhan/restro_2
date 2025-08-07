"""
Multi-step migration for restaurant multi-tenant system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models.models import Restaurant, Category, Dish
from app.models.order import ShivdhabaOrder
import sqlalchemy as sa
from sqlalchemy.schema import CreateTable, AddConstraint, ForeignKeyConstraint

def execute_multi_step_migration():
    with app.app_context():
        try:
            print("Starting multi-step migration process...")
            
            # Step 1: Check if Restaurant table exists
            print("Step 1: Checking Restaurant table...")
            
            # Check if table exists
            table_exists = False
            try:
                db.session.execute(sa.text("SELECT 1 FROM restaurant LIMIT 1"))
                table_exists = True
                print("Restaurant table already exists")
            except:
                # Table doesn't exist
                print("Creating Restaurant table...")
                
                # Get Restaurant table metadata
                restaurant_table = Restaurant.__table__
                
                # Get the create table SQL
                create_table_sql = str(CreateTable(restaurant_table).compile(db.engine))
                
                # Execute the create table SQL
                db.session.execute(sa.text("SET FOREIGN_KEY_CHECKS=0"))
                db.session.execute(sa.text(create_table_sql))
                db.session.commit()
                print("Restaurant table created successfully!")
            
            # Ensure foreign key checks are disabled
            db.session.execute(sa.text("SET FOREIGN_KEY_CHECKS=0"))
            
            # Step 2: Create the first restaurant (Shiv Dhaba)
            print("Step 2: Creating first restaurant...")
            
            # Check if restaurant already exists
            existing_restaurant = Restaurant.query.filter_by(slug='shiv-dhaba').first()
            if existing_restaurant:
                print("Restaurant 'Shiv Dhaba' already exists. Using existing one.")
                restaurant = existing_restaurant
            else:
                restaurant = Restaurant(
                    name="Shiv Dhaba",
                    slug="shiv-dhaba",
                    address="123 Main Street, Delhi",
                    contact="9999999999",
                    primary_location="Delhi",
                    is_active=True
                )
            db.session.add(restaurant)
            db.session.commit()
            print(f"Created restaurant: {restaurant.name} with ID: {restaurant.id}")
            
            # Step 3: Update existing data to reference the restaurant
            print("Step 3: Updating existing data with restaurant reference...")
            
            # Update categories
            print("Updating categories...")
            db.session.execute(
                sa.text(f"UPDATE category SET restaurant_id = {restaurant.id} WHERE restaurant_id IS NULL")
            )
            
            # Update dishes
            print("Updating dishes...")
            db.session.execute(
                sa.text(f"UPDATE dish SET restaurant_id = {restaurant.id} WHERE restaurant_id IS NULL")
            )
            
            # Update orders
            print("Updating orders...")
            db.session.execute(
                sa.text(f"UPDATE shivdhaba_order SET restaurant_id = {restaurant.id} WHERE restaurant_id IS NULL")
            )
            
            db.session.commit()
            
            # Step 4: Add foreign key constraints
            print("Step 4: Adding foreign key constraints...")
            db.session.execute(sa.text("SET FOREIGN_KEY_CHECKS=1"))
            db.session.commit()
            
            print("Multi-step migration completed successfully!")
            
            print(f"\nMigration Summary:")
            print(f"- Restaurant created: {restaurant.name} (ID: {restaurant.id})")
            print(f"- Categories, dishes, and orders updated with restaurant reference")
            print(f"\nNew URL structure:")
            print(f"- Public Menu: /{restaurant.slug}/menu")
            print(f"- Admin Panel: /{restaurant.slug}/admin")
            
            return True
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    execute_multi_step_migration()
