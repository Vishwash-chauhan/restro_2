# Restaurant Admin Management (restro_2)

A Flask-based web application for restaurant admin management. It provides CRUD operations for dishes and categories, an admin dashboard, and uses MySQL for data storage.

## Features
- Admin dashboard with summary
- CRUD for dishes (add, edit, delete, list)
- CRUD for categories
- Dish fields: name, image, description, price (half/full), category, is_available, is_vegetarian, spice_level
- Image upload and storage in static folder
- SQLAlchemy ORM for models and database
- Flask-WTF for forms and CSRF protection
- Bootstrap for simple styling
- Modular code structure

## Tech Stack
- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Migrate
- MySQL (with PyMySQL)
- Bootstrap 5

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone https://github.com/Vishwash-chauhan/restro_2.git
   cd restro_2
   ```
2. **Create and activate a virtual environment**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure MySQL**
   - Ensure MySQL is running and create a database named `restaurant_db`.
   - Update credentials in `app/__init__.py` if needed.
5. **Run migrations**
   ```sh
   $env:FLASK_APP = "app"
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. **Seed sample data (optional)**
   ```sh
   python seed_data.py
   ```
7. **Start the app**
   ```sh
   python run.py
   ```
   Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Folder Structure
```
app/
  __init__.py
  models/
    models.py
  forms/
    forms.py
  templates/
    ...
  static/
    images/
run.py
seed_data.py
show_data.py
migrations/
.gitignore
README.md
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
