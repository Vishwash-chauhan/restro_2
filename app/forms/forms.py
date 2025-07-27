from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, BooleanField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional

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
