from app import app, db
from app.models.models import Category, Dish

with app.app_context():
    print('Categories:')
    for category in Category.query.all():
        print(f"ID: {category.id}, Name: {category.name}, Created At: {category.created_at}, Deleted At: {category.deleted_at}")
    print('\nDishes:')
    for dish in Dish.query.all():
        print(f"ID: {dish.id}, Name: {dish.name}, Category: {dish.category_id}, Created At: {dish.created_at}, Deleted At: {dish.deleted_at}")
