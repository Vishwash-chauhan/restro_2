from flask import Blueprint, render_template, request
from app.models.models import Dish, Category

public_bp = Blueprint('public', __name__, template_folder='templates/public')

@public_bp.route('/shivdhaba')
def menu():
    category_id = request.args.get('category', type=int)
    categories = Category.query.all()
    if category_id:
        dishes = Dish.query.filter_by(category_id=category_id, is_available=True).all()
    else:
        dishes = Dish.query.filter_by(is_available=True).all()
    return render_template('public_menu.html', categories=categories, dishes=dishes, selected_category=category_id)
