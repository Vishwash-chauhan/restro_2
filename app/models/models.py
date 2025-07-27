from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    dishes = db.relationship('Dish', backref='category', lazy=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))
    description = db.Column(db.Text)
    price_half = db.Column(db.Float)
    price_full = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    is_vegetarian = db.Column(db.Boolean, default=False)
    spice_level = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
