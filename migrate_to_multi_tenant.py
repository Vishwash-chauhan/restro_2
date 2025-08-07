"""
Migration script to convert single-tenant app to multi-tenant
This script will:
1. Run the migration to create the Restaurant table and add relationship columns
2. Create the first restaurant entry for existing data
3. Update existing data with the restaurant reference

IMPORTANT: This script should be run AFTER the database migration is complete
"""

import sys
import os
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models.models import Restaurant, Category, Dish
from app.models.order import ShivdhabaOrder

def migrate_to_multi_tenant():
    # First run the migrations to create the tables
    print("Step 1: Ensure migrations are up-to-date")
    try:
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
        env["FLASK_APP"] = "run.py"
        
        # Run the upgrade command to ensure tables exist
        upgrade_cmd = "flask db upgrade"
        print(f"Executing: {upgrade_cmd}")
        
        upgrade_process = subprocess.run(
            upgrade_cmd,
            shell=True,
            env=env,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True
        )
        
        if upgrade_process.returncode != 0:
            print("Migration upgrade failed:")
            print(upgrade_process.stderr)
            return False
            
        print(upgrade_process.stdout)
    except Exception as e:
        print(f"Migration error: {str(e)}")
        return False
    
    # Now perform the data migration
    print("Step 2: Migrating data to multi-tenant structure")
    with app.app_context():
        # Step 1: Create the first restaurant (Shiv Dhaba)
        print("Creating first restaurant...")
        
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
                contact_phone="9999999999",
                contact_email="admin@shivdhaba.com",
                description="Traditional Indian cuisine with authentic flavors",
                is_active=True
            )
            db.session.add(restaurant)
            db.session.commit()
            print(f"Created restaurant: {restaurant.name} with ID: {restaurant.id}")
        
        # Step 2: Update existing categories
        print("Updating categories...")
        categories = Category.query.filter_by(restaurant_id=None).all()
        for category in categories:
            category.restaurant_id = restaurant.id
            print(f"Updated category: {category.name}")
        
        # Step 3: Update existing dishes
        print("Updating dishes...")
        dishes = Dish.query.filter_by(restaurant_id=None).all()
        for dish in dishes:
            dish.restaurant_id = restaurant.id
            print(f"Updated dish: {dish.name}")
        
        # Step 4: Update existing orders
        print("Updating orders...")
        orders = ShivdhabaOrder.query.filter_by(restaurant_id=None).all()
        for order in orders:
            order.restaurant_id = restaurant.id
            print(f"Updated order ID: {order.id}")
        
        # Commit all changes
        db.session.commit()
        print("Migration completed successfully!")
        
        print(f"\nMigration Summary:")
        print(f"- Restaurant created: {restaurant.name} (ID: {restaurant.id})")
        print(f"- Categories updated: {len(categories)}")
        print(f"- Dishes updated: {len(dishes)}")
        print(f"- Orders updated: {len(orders)}")
        print(f"\nNew URL structure:")
        print(f"- Public Menu: /{restaurant.slug}/menu")
        print(f"- Admin Panel: /{restaurant.slug}/admin")
        
        return True

if __name__ == "__main__":
    migrate_to_multi_tenant()
