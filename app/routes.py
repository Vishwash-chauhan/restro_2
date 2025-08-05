from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models.models import Dish, Category
from app.forms.forms import DishForm, CategoryForm
import os
from werkzeug.utils import secure_filename
import uuid

# Admin order management imports
from app.models.order import ShivdhabaOrder
from flask import jsonify, request
from sqlalchemy import desc
import json

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def dashboard():
    dish_count = Dish.query.count()
    category_count = Category.query.count()
    return render_template('dashboard.html', dish_count=dish_count, category_count=category_count)

@app.route('/admin/orders')
def admin_orders_today():
    from datetime import datetime, timedelta
    today = datetime.now().date()
    orders_today = ShivdhabaOrder.query.filter(
        ShivdhabaOrder.created_at >= today,
        ShivdhabaOrder.created_at < today + timedelta(days=1)
    ).order_by(desc(ShivdhabaOrder.created_at)).all()
    return render_template('orders.html', orders_today=orders_today)

# Previous orders (yesterday and earlier)
@app.route('/admin/orders/previous')
def admin_orders_previous():
    from datetime import datetime, timedelta
    today = datetime.now().date()
    orders_prev = ShivdhabaOrder.query.filter(
        ShivdhabaOrder.created_at < today
    ).order_by(desc(ShivdhabaOrder.created_at)).all()
    return render_template('orders_prev.html', orders_prev=orders_prev)
    from datetime import datetime, timedelta
    today = datetime.now().date()
    orders_today = ShivdhabaOrder.query.filter(
        ShivdhabaOrder.created_at >= today,
        ShivdhabaOrder.created_at < today + timedelta(days=1)
    ).order_by(desc(ShivdhabaOrder.created_at)).all()
    return render_template('orders.html', orders_today=orders_today)

# AJAX: Toggle delivered status
@app.route('/admin/orders/toggle-delivered/<int:order_id>', methods=['POST'])
def toggle_order_delivered(order_id):
    order = ShivdhabaOrder.query.get_or_404(order_id)
    order.delivered = not order.delivered
    from app import db
    db.session.commit()
    return jsonify({'success': True, 'delivered': order.delivered})

# AJAX: Get order details
@app.route('/admin/orders/details/<int:order_id>')
def get_order_details(order_id):
    order = ShivdhabaOrder.query.get_or_404(order_id)
    items = json.loads(order.items)
    return jsonify({
        'id': order.id,
        'name': order.name,
        'mobile': order.mobile,
        'address': order.address,
        'instructions': order.instructions,
        'items': items,
        'total': order.total,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else '',
        'delivered': order.delivered
    })
@app.route('/dishes')
def list_dishes():
    dishes = Dish.query.all()
    return render_template('list_dishes.html', dishes=dishes)

@app.route('/dishes/add', methods=['GET', 'POST'])
def add_dish():
    form = DishForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            original_filename = secure_filename(form.image.data.filename)
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            form.image.data.save(image_path)
            filename = unique_filename
        dish = Dish(
            name=form.name.data,
            image=filename,
            description=form.description.data,
            price_half=form.price_half.data,
            price_full=form.price_full.data,
            category_id=form.category_id.data,
            is_available=form.is_available.data,
            is_vegetarian=form.is_vegetarian.data,
            spice_level=form.spice_level.data
        )
        db.session.add(dish)
        db.session.commit()
        flash('Dish added successfully!', 'success')
        return redirect(url_for('list_dishes'))
    return render_template('dish_form.html', form=form, action='Add')

@app.route('/dishes/edit/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    form = DishForm(obj=dish)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        if form.image.data:
            original_filename = secure_filename(form.image.data.filename)
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            form.image.data.save(image_path)
            dish.image = unique_filename
        dish.name = form.name.data
        dish.description = form.description.data
        dish.price_half = form.price_half.data
        dish.price_full = form.price_full.data
        dish.category_id = form.category_id.data
        dish.is_available = form.is_available.data
        dish.is_vegetarian = form.is_vegetarian.data
        dish.spice_level = form.spice_level.data
        db.session.commit()
        flash('Dish updated successfully!', 'success')
        return redirect(url_for('list_dishes'))
    return render_template('dish_form.html', form=form, action='Edit')

@app.route('/dishes/delete/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    flash('Dish deleted!', 'success')
    return redirect(url_for('list_dishes'))

@app.route('/categories')
def list_categories():
    categories = Category.query.all()
    return render_template('list_categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added!', 'success')
        return redirect(url_for('list_categories'))
    return render_template('category_form.html', form=form, action='Add')

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated!', 'success')
        return redirect(url_for('list_categories'))
    return render_template('category_form.html', form=form, action='Edit')

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted!', 'success')
    return redirect(url_for('list_categories'))

@app.route('/dishes/toggle-availability/<int:dish_id>', methods=['POST'])
def toggle_dish_availability(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    dish.is_available = not dish.is_available
    db.session.commit()
    
    status = "available" if dish.is_available else "unavailable"
    return jsonify({
        'success': True,
        'is_available': dish.is_available,
        'message': f'Dish marked as {status}'
    })
