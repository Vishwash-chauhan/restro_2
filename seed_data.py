from app import app, db
from app.models.models import Category, Dish

sample_categories = [
    'Starters',
    'Main Course',
    'Desserts',
    'Beverages'
]

sample_dishes = [
    {
        'name': 'Paneer Tikka',
        'image': None,
        'description': 'Grilled paneer cubes marinated in spices.',
        'price_half': 120.0,
        'price_full': 220.0,
        'is_available': True,
        'is_vegetarian': True,
        'spice_level': 'Medium',
        'category': 'Starters'
    },
    {
        'name': 'Chicken Curry',
        'image': None,
        'description': 'Spicy chicken curry with rich gravy.',
        'price_half': 150.0,
        'price_full': 280.0,
        'is_available': True,
        'is_vegetarian': False,
        'spice_level': 'Hot',
        'category': 'Main Course'
    },
    {
        'name': 'Gulab Jamun',
        'image': None,
        'description': 'Sweet milk dumplings in sugar syrup.',
        'price_half': 60.0,
        'price_full': 110.0,
        'is_available': True,
        'is_vegetarian': True,
        'spice_level': 'Mild',
        'category': 'Desserts'
    },
    {
        'name': 'Masala Lemonade',
        'image': None,
        'description': 'Refreshing lemonade with spices.',
        'price_half': 40.0,
        'price_full': 70.0,
        'is_available': True,
        'is_vegetarian': True,
        'spice_level': 'Mild',
        'category': 'Beverages'
    }
]

with app.app_context():
    # Insert categories
    category_objs = {}
    for cat_name in sample_categories:
        category = Category(name=cat_name)
        db.session.add(category)
        category_objs[cat_name] = category
    db.session.commit()

    # Insert dishes
    for dish in sample_dishes:
        dish_obj = Dish(
            name=dish['name'],
            image=dish['image'],
            description=dish['description'],
            price_half=dish['price_half'],
            price_full=dish['price_full'],
            is_available=dish['is_available'],
            is_vegetarian=dish['is_vegetarian'],
            spice_level=dish['spice_level'],
            category_id=category_objs[dish['category']].id
        )
        db.session.add(dish_obj)
    db.session.commit()

print('Sample categories and dishes inserted.')
