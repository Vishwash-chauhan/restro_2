"""
Generate migration for multi-tenant restaurant system using Python Alembic API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, migrate
from alembic import command
from alembic.config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run database migrations using Alembic API directly"""
    try:
        print("Starting database migration process...")
        
        # Get alembic.ini path
        alembic_ini = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations', 'alembic.ini')
        if not os.path.exists(alembic_ini):
            print(f"Error: alembic.ini not found at {alembic_ini}")
            return False
        
        # Create an Alembic config
        alembic_cfg = Config(alembic_ini)
        
        # Set script_location
        script_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
        alembic_cfg.set_main_option('script_location', script_location)
        
        with app.app_context():
            # Step 1: Create a new migration
            print("Step 1: Creating migration revision for multi-tenant structure")
            try:
                command.revision(
                    alembic_cfg,
                    message="Add restaurant model and relationships",
                    autogenerate=True
                )
                print("Migration revision created successfully")
            except Exception as e:
                print(f"Error creating migration: {str(e)}")
                return False
            
            # Step 2: Apply the migration
            print("Step 2: Applying migration to database")
            try:
                command.upgrade(alembic_cfg, "head")
                print("Database upgraded successfully")
            except Exception as e:
                print(f"Error upgrading database: {str(e)}")
                return False
            
            print("Migration process completed successfully!")
            return True
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    run_migrations()
