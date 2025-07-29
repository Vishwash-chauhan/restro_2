from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.models import Dish, Category

public_bp = Blueprint('public', __name__, template_folder='templates/public')

@public_bp.route('/shivdhaba')
def menu():
    # Test session persistence
    session['test_key'] = session.get('test_key', 0) + 1
    print('SESSION TEST VALUE:', session['test_key'])
    category_id = request.args.get('category', type=int)
    categories = Category.query.all()
    if category_id:
        dishes = Dish.query.filter_by(category_id=category_id, is_available=True).all()
    else:
        dishes = Dish.query.filter_by(is_available=True).all()
    # Calculate cart_count
    cart = session.get('cart', {})
    cart_count = sum((item.get('half', 0) + item.get('full', 0)) for item in cart.values())
    return render_template('/public/public_menu.html', categories=categories, dishes=dishes, selected_category=category_id, session_test=session['test_key'], cart_count=cart_count)

@public_bp.route('/shivdhaba/dish/<int:dish_id>')
def dish_detail(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    return render_template('dish_detail.html', dish=dish)

@public_bp.route('/shivdhaba/cart')
def view_cart():
    cart = session.get('cart', {})
    total = 0
    cart_items = []
    for dish_id, item in cart.items():
        dish = Dish.query.get(dish_id)
        if not dish:
            continue
        item_total = (item.get('half', 0) * dish.price_half if dish.price_half else 0) + (item.get('full', 0) * dish.price_full if dish.price_full else 0)
        total += item_total
        cart_items.append({
            'id': dish_id,
            'name': dish.name,
            'image': dish.image,
            'category': dish.category.name,
            'half': item.get('half', 0),
            'full': item.get('full', 0),
            'price_half': dish.price_half,
            'price_full': dish.price_full,
            'item_total': item_total
        })
    return render_template('cart.html', cart_items=cart_items, total=total)

@public_bp.route('/shivdhaba/cart/add/<int:dish_id>', methods=['POST'])
def add_to_cart(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    half_qty = int(request.form.get('half_qty', 0))
    full_qty = int(request.form.get('full_qty', 0))
    cart = session.get('cart', {})
    if str(dish_id) not in cart:
        cart[str(dish_id)] = {'half': 0, 'full': 0}
    cart[str(dish_id)]['half'] += half_qty
    cart[str(dish_id)]['full'] += full_qty
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('public.menu'))

@public_bp.route('/shivdhaba/cart/update/<int:dish_id>', methods=['POST'])
def update_cart(dish_id):
    cart = session.get('cart', {})
    if str(dish_id) in cart:
        cart[str(dish_id)]['half'] = int(request.form.get('half_qty', 0))
        cart[str(dish_id)]['full'] = int(request.form.get('full_qty', 0))
        session['cart'] = cart
        flash('Cart updated!', 'success')
    return redirect(url_for('public.view_cart'))

@public_bp.route('/shivdhaba/cart/remove/<int:dish_id>', methods=['POST'])
def remove_from_cart(dish_id):
    cart = session.get('cart', {})
    if str(dish_id) in cart:
        del cart[str(dish_id)]
        session['cart'] = cart
        flash('Item removed from cart!', 'success')
    return redirect(url_for('public.view_cart'))
