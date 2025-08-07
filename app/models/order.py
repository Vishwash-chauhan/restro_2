from app import db

class ShivdhabaOrder(db.Model):
    __tablename__ = 'shivdhaba_order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text)
    items = db.Column(db.Text, nullable=False)  # Store as JSON string
    total = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    delivered = db.Column(db.Boolean, default=False, nullable=False)
