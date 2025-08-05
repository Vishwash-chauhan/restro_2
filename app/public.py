from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models.models import Dish, Category

public_bp = Blueprint('public', __name__, template_folder='templates/public')

@public_bp.route('/shivdhaba')
def old_menu():
    return redirect(url_for('public.menu'))

@public_bp.route('/shivdhaba/menu')
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
    # Calculate cart_count and get cart quantities
    cart = session.get('cart', {})
    cart_count = sum((item.get('half', 0) + item.get('full', 0)) for item in cart.values())
    return render_template('/public/public_menu.html', categories=categories, dishes=dishes, selected_category=category_id, session_test=session['test_key'], cart_count=cart_count, cart=cart)

@public_bp.route('/shivdhaba/dish/<int:dish_id>')
def dish_detail(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    # Get cart quantities for this specific dish
    cart = session.get('cart', {})
    cart_count = sum((item.get('half', 0) + item.get('full', 0)) for item in cart.values())
    dish_cart = cart.get(str(dish_id), {'half': 0, 'full': 0})
    return render_template('dish_detail.html', dish=dish, cart_count=cart_count, dish_cart=dish_cart)

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

from app.models.order import ShivdhabaOrder
import json
import re

@public_bp.route('/shivdhaba/cart/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    total = 0
    items = []
    for dish_id, item in cart.items():
        dish = Dish.query.get(dish_id)
        if not dish:
            continue
        item_total = (item.get('half', 0) * dish.price_half if dish.price_half else 0) + (item.get('full', 0) * dish.price_full if dish.price_full else 0)
        total += item_total
        items.append({
            'id': dish_id,
            'name': dish.name,
            'half': item.get('half', 0),
            'full': item.get('full', 0),
            'price_half': dish.price_half,
            'price_full': dish.price_full,
            'item_total': item_total
        })
    name = request.form.get('name', '').strip()
    mobile = request.form.get('mobile', '').strip()
    address = request.form.get('address', '').strip()
    instructions = request.form.get('instructions', '').strip()
    # Mobile validation: 10 digits, starts with 6-9
    if not re.match(r'^[6-9]\d{9}$', mobile):
        flash('Invalid mobile number. Please enter a valid 10-digit mobile number starting with 6-9.', 'danger')
        return redirect(url_for('public.view_cart'))
    if not name or not address:
        flash('Name and address are required.', 'danger')
        return redirect(url_for('public.view_cart'))
    order = ShivdhabaOrder(
        name=name,
        mobile=mobile,
        address=address,
        instructions=instructions,
        items=json.dumps(items),
        total=total
    )
    from app import db
    db.session.add(order)
    db.session.commit()
    session['cart'] = {}
    flash('Order placed successfully! Thank you for ordering.', 'success')
    return redirect(url_for('public.order_success', order_id=order.id))
# Order success page
@public_bp.route('/shivdhaba/order-success/<int:order_id>')
def order_success(order_id):
    return render_template('public/order_success.html', order_id=order_id)

# Download order details
@public_bp.route('/shivdhaba/download-order/<int:order_id>')
def download_order(order_id):
    from app.models.order import ShivdhabaOrder
    import io, json
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    order = ShivdhabaOrder.query.get(order_id)
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('public.menu'))
    items = json.loads(order.items)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle('Shiv Dhaba')
    width, height = letter
    y = height - 40
    c.setFont('Helvetica-Bold', 18)
    c.drawString(40, y, 'Order Receipt')
    y -= 30
    c.setFont('Helvetica', 12)
    c.drawString(40, y, f"Order ID: {order.id}")
    y -= 20
    c.drawString(40, y, f"Placed At: {order.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(order, 'created_at') and order.created_at else 'N/A'}")
    y -= 20
    c.drawString(40, y, f"Name: {order.name}")
    y -= 20
    c.drawString(40, y, f"Mobile: {order.mobile}")
    y -= 20
    c.drawString(40, y, f"Address: {order.address}")
    y -= 30
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, y, 'Items:')
    y -= 20
    c.setFont('Helvetica', 12)
    for item in items:
        item_line = f"{item['name']}  (Half: {item['half']}, Full: {item['full']})  Rs.{item['item_total']}"
        c.drawString(50, y, item_line)
        y -= 18
        if y < 60:
            c.showPage()
            y = height - 40
            c.setFont('Helvetica', 12)
    y -= 10
    c.setFont('Helvetica-Bold', 13)
    c.drawString(40, y, f"Total: Rs.{order.total}")
    c.showPage()
    c.save()
    buffer.seek(0)
    from flask import send_file
    return send_file(buffer, as_attachment=True, download_name=f'Shiv Dhaba Order {order.id}.pdf', mimetype='application/pdf')

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

@public_bp.route('/shivdhaba/cart/update-quantity/<int:dish_id>', methods=['POST'])
def update_quantity(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    data = request.get_json()
    portion = data.get('portion')  # 'half' or 'full'
    action = data.get('action')    # 'increase' or 'decrease'
    
    cart = session.get('cart', {})
    if str(dish_id) not in cart:
        cart[str(dish_id)] = {'half': 0, 'full': 0}
    
    if action == 'increase':
        cart[str(dish_id)][portion] += 1
    elif action == 'decrease':
        cart[str(dish_id)][portion] = max(0, cart[str(dish_id)][portion] - 1)
    
    # Remove item from cart if both quantities are 0
    if cart[str(dish_id)]['half'] == 0 and cart[str(dish_id)]['full'] == 0:
        del cart[str(dish_id)]
    
    session['cart'] = cart
    
    # Calculate new cart count
    cart_count = sum((item.get('half', 0) + item.get('full', 0)) for item in cart.values())
    
    return jsonify({
        'success': True,
        'cart_count': cart_count,
        'item_half': cart[str(dish_id)]['half'] if str(dish_id) in cart else 0,
        'item_full': cart[str(dish_id)]['full'] if str(dish_id) in cart else 0
    })

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
