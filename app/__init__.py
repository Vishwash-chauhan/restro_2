from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/restaurant_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app.public import public_bp
app.register_blueprint(public_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
