from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, BooleanField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, ValidationError
import re

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired(), Length(min=2, max=100)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(min=2, max=100)])
    address = TextAreaField('Address', validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=20)])
    primary_location = StringField('Primary Location', validators=[DataRequired(), Length(max=100)])
    logo = FileField('Logo', validators=[Optional()])
    brand_color = StringField('Brand Color', validators=[Optional(), Length(max=7)], default='#3B82F6')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
    
    def validate_slug(self, field):
        # Only allow lowercase letters, numbers, and hyphens
        if not re.match(r'^[a-z0-9-]+$', field.data):
            raise ValidationError('Slug can only contain lowercase letters, numbers, and hyphens.')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class DishForm(FlaskForm):
    name = StringField('Dish Name', validators=[DataRequired()])
    image = FileField('Image', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    price_half = FloatField('Price (Half)', validators=[Optional()])
    price_full = FloatField('Price (Full)', validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    is_available = BooleanField('Available')
    is_vegetarian = BooleanField('Vegetarian')
    spice_level = SelectField('Spice Level', choices=[('Mild', 'Mild'), ('Medium', 'Medium'), ('Hot', 'Hot')], validators=[Optional()])
    submit = SubmitField('Save')
