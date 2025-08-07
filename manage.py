"""
Flask command script to run migrations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# Initialize Flask-Migrate
migrate = Migrate(app, db)
manager = Manager(app)

# Add the Flask-Migrate commands to the manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
