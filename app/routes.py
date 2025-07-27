from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models.models import Dish, Category
from app.forms.forms import DishForm, CategoryForm
import os
from werkzeug.utils import secure_filename

@app.route('/')
def dashboard():
    dish_count = Dish.query.count()
    category_count = Category.query.count()
    return render_template('dashboard.html', dish_count=dish_count, category_count=category_count)

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
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dish.image = filename
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
