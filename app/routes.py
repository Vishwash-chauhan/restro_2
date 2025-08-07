from flask import render_template, redirect, url_for, request, flash, abort
from app import app, db
from app.models.models import Dish, Category, Restaurant
from app.forms.forms import DishForm, CategoryForm, RestaurantForm
import os
from werkzeug.utils import secure_filename
import uuid
import re

# Admin order management imports
from app.models.order import ShivdhabaOrder
from flask import jsonify, request
from sqlalchemy import desc
import json

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to get restaurant by slug
def get_restaurant_by_slug(slug):
    restaurant = Restaurant.query.filter_by(slug=slug, is_active=True).first()
    if not restaurant:
        abort(404, description=f"Restaurant '{slug}' not found")
    return restaurant

# Helper function to generate slug from name
def generate_slug(name):
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name)
    slug = re.sub(r'\s+', '-', slug)
    slug = slug.lower().strip('-')
    return slug

# ==================== SUPER ADMIN ROUTES ====================
@app.route('/')
def super_admin_dashboard():
    restaurant_count = Restaurant.query.count()
    total_dishes = Dish.query.count()
    total_orders = ShivdhabaOrder.query.count()
    return render_template('super_admin/dashboard.html', 
                         restaurant_count=restaurant_count,
                         total_dishes=total_dishes, 
                         total_orders=total_orders)

@app.route('/super-admin/restaurants')
def list_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('super_admin/list_restaurants.html', restaurants=restaurants)

@app.route('/super-admin/restaurants/add', methods=['GET', 'POST'])
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        # Check if slug already exists
        existing = Restaurant.query.filter_by(slug=form.slug.data).first()
        if existing:
            flash('A restaurant with this URL slug already exists. Please choose a different slug.', 'danger')
            return render_template('super_admin/restaurant_form.html', form=form, action='Add')
        
        filename = None
        if form.logo.data:
            original_filename = secure_filename(form.logo.data.filename)
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            form.logo.data.save(image_path)
            filename = unique_filename
            
        restaurant = Restaurant(
            name=form.name.data,
            slug=form.slug.data,
            address=form.address.data,
            contact=form.contact.data,
            primary_location=form.primary_location.data,
            logo=filename,
            brand_color=form.brand_color.data,
            is_active=form.is_active.data
        )
        db.session.add(restaurant)
        db.session.commit()
        flash(f'Restaurant "{restaurant.name}" added successfully!', 'success')
        return redirect(url_for('list_restaurants'))
    
    # Auto-generate slug from name if not provided
    if request.method == 'GET' and request.args.get('name'):
        form.slug.data = generate_slug(request.args.get('name'))
    
    return render_template('super_admin/restaurant_form.html', form=form, action='Add')

@app.route('/super-admin/restaurants/edit/<int:restaurant_id>', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    form = RestaurantForm(obj=restaurant)
    
    if form.validate_on_submit():
        # Check if slug already exists (excluding current restaurant)
        existing = Restaurant.query.filter(
            Restaurant.slug == form.slug.data,
            Restaurant.id != restaurant_id
        ).first()
        if existing:
            flash('A restaurant with this URL slug already exists. Please choose a different slug.', 'danger')
            return render_template('super_admin/restaurant_form.html', form=form, action='Edit')
        
        if form.logo.data:
            original_filename = secure_filename(form.logo.data.filename)
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            form.logo.data.save(image_path)
            restaurant.logo = unique_filename
            
        restaurant.name = form.name.data
        restaurant.slug = form.slug.data
        restaurant.address = form.address.data
        restaurant.contact = form.contact.data
        restaurant.primary_location = form.primary_location.data
        restaurant.brand_color = form.brand_color.data
        restaurant.is_active = form.is_active.data
        
        db.session.commit()
        flash(f'Restaurant "{restaurant.name}" updated successfully!', 'success')
        return redirect(url_for('list_restaurants'))
    
    return render_template('super_admin/restaurant_form.html', form=form, action='Edit')

@app.route('/super-admin/restaurants/delete/<int:restaurant_id>', methods=['POST'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    restaurant_name = restaurant.name
    db.session.delete(restaurant)
    db.session.commit()
    flash(f'Restaurant "{restaurant_name}" deleted successfully!', 'success')
    return redirect(url_for('list_restaurants'))

# ==================== RESTAURANT-SPECIFIC ROUTES ====================

# ==================== RESTAURANT-SPECIFIC ROUTES ====================

# Restaurant Admin Dashboard
@app.route('/<slug>/admin')
def restaurant_admin_dashboard(slug):
    restaurant = get_restaurant_by_slug(slug)
    dish_count = Dish.query.filter_by(restaurant_id=restaurant.id).count()
    category_count = Category.query.filter_by(restaurant_id=restaurant.id).count()
    order_count = ShivdhabaOrder.query.filter_by(restaurant_id=restaurant.id).count()
    return render_template('admin/dashboard.html', 
                         restaurant=restaurant,
                         dish_count=dish_count, 
                         category_count=category_count, 
                         order_count=order_count)

# Orders Management
@app.route('/<slug>/admin/orders')
def admin_orders_today(slug):
    restaurant = get_restaurant_by_slug(slug)
    from datetime import datetime, timedelta
    today = datetime.now().date()
    orders_today = ShivdhabaOrder.query.filter(
        ShivdhabaOrder.restaurant_id == restaurant.id,
        ShivdhabaOrder.created_at >= today,
        ShivdhabaOrder.created_at < today + timedelta(days=1)
    ).order_by(desc(ShivdhabaOrder.created_at)).all()
    return render_template('admin/orders.html', restaurant=restaurant, orders_today=orders_today)

@app.route('/<slug>/admin/orders/previous')
def admin_orders_previous(slug):
    restaurant = get_restaurant_by_slug(slug)
    from datetime import datetime, timedelta
    today = datetime.now().date()
    orders_prev = ShivdhabaOrder.query.filter(
        ShivdhabaOrder.restaurant_id == restaurant.id,
        ShivdhabaOrder.created_at < today
    ).order_by(desc(ShivdhabaOrder.created_at)).all()
    return render_template('admin/orders_prev.html', restaurant=restaurant, orders_prev=orders_prev)

@app.route('/<slug>/admin/orders/toggle-delivered/<int:order_id>', methods=['POST'])
def toggle_order_delivered(slug, order_id):
    restaurant = get_restaurant_by_slug(slug)
    order = ShivdhabaOrder.query.filter_by(id=order_id, restaurant_id=restaurant.id).first_or_404()
    order.delivered = not order.delivered
    db.session.commit()
    return jsonify({'success': True, 'delivered': order.delivered})

@app.route('/<slug>/admin/orders/details/<int:order_id>')
def get_order_details(slug, order_id):
    restaurant = get_restaurant_by_slug(slug)
    order = ShivdhabaOrder.query.filter_by(id=order_id, restaurant_id=restaurant.id).first_or_404()
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
# Dishes Management
@app.route('/<slug>/admin/dishes')
def list_dishes(slug):
    restaurant = get_restaurant_by_slug(slug)
    dishes = Dish.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('admin/list_dishes.html', restaurant=restaurant, dishes=dishes)

@app.route('/<slug>/admin/dishes/add', methods=['GET', 'POST'])
def add_dish(slug):
    restaurant = get_restaurant_by_slug(slug)
    form = DishForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(restaurant_id=restaurant.id).all()]
    
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
            restaurant_id=restaurant.id,
            is_available=form.is_available.data,
            is_vegetarian=form.is_vegetarian.data,
            spice_level=form.spice_level.data
        )
        db.session.add(dish)
        db.session.commit()
        flash('Dish added successfully!', 'success')
        return redirect(url_for('list_dishes', slug=slug))
    return render_template('admin/dish_form.html', restaurant=restaurant, form=form, action='Add')

@app.route('/<slug>/admin/dishes/edit/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(slug, dish_id):
    restaurant = get_restaurant_by_slug(slug)
    dish = Dish.query.filter_by(id=dish_id, restaurant_id=restaurant.id).first_or_404()
    form = DishForm(obj=dish)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(restaurant_id=restaurant.id).all()]
    
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
        return redirect(url_for('list_dishes', slug=slug))
    return render_template('admin/dish_form.html', restaurant=restaurant, form=form, action='Edit')

@app.route('/<slug>/admin/dishes/delete/<int:dish_id>', methods=['POST'])
def delete_dish(slug, dish_id):
    restaurant = get_restaurant_by_slug(slug)
    dish = Dish.query.filter_by(id=dish_id, restaurant_id=restaurant.id).first_or_404()
    db.session.delete(dish)
    db.session.commit()
    flash('Dish deleted!', 'success')
    return redirect(url_for('list_dishes', slug=slug))

@app.route('/<slug>/admin/dishes/toggle-availability/<int:dish_id>', methods=['POST'])
def toggle_dish_availability(slug, dish_id):
    restaurant = get_restaurant_by_slug(slug)
    dish = Dish.query.filter_by(id=dish_id, restaurant_id=restaurant.id).first_or_404()
    dish.is_available = not dish.is_available
    db.session.commit()
    
    status = "available" if dish.is_available else "unavailable"
    return jsonify({
        'success': True,
        'is_available': dish.is_available,
        'message': f'Dish marked as {status}'
    })

# Categories Management
@app.route('/<slug>/admin/categories')
def list_categories(slug):
    restaurant = get_restaurant_by_slug(slug)
    categories = Category.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('admin/list_categories.html', restaurant=restaurant, categories=categories)

@app.route('/<slug>/admin/categories/add', methods=['GET', 'POST'])
def add_category(slug):
    restaurant = get_restaurant_by_slug(slug)
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, restaurant_id=restaurant.id)
        db.session.add(category)
        db.session.commit()
        flash('Category added!', 'success')
        return redirect(url_for('list_categories', slug=slug))
    return render_template('admin/category_form.html', restaurant=restaurant, form=form, action='Add')

@app.route('/<slug>/admin/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(slug, category_id):
    restaurant = get_restaurant_by_slug(slug)
    category = Category.query.filter_by(id=category_id, restaurant_id=restaurant.id).first_or_404()
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated!', 'success')
        return redirect(url_for('list_categories', slug=slug))
    return render_template('admin/category_form.html', restaurant=restaurant, form=form, action='Edit')

@app.route('/<slug>/admin/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(slug, category_id):
    restaurant = get_restaurant_by_slug(slug)
    category = Category.query.filter_by(id=category_id, restaurant_id=restaurant.id).first_or_404()
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted!', 'success')
    return redirect(url_for('list_categories', slug=slug))
