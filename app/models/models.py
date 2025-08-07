from app import db

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    primary_location = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(200))
    brand_color = db.Column(db.String(7), default='#3B82F6')  # Default blue
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    categories = db.relationship('Category', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    dishes = db.relationship('Dish', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('ShivdhabaOrder', backref='restaurant', lazy=True, cascade='all, delete-orphan')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
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
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
