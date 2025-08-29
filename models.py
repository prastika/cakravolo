from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='viewer')  # admin, manager, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    area_hectares = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200))
    established_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CensusOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    entity = db.Column(db.String(100), nullable=False)
    census_type = db.Column(db.String(100), nullable=False)  # oil palm flower & fruit | oil palm tree
    tree_image_url = db.Column(db.String(200))
    hectare_covered = db.Column(db.Float, nullable=False)
    prediction_result = db.Column(db.Text)
    action_recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CensusData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.String(50), db.ForeignKey('census_operation.operation_id'), nullable=False)
    male_flower = db.Column(db.Integer, default=0)
    female_flower = db.Column(db.Integer, default=0)
    purse_flower = db.Column(db.Integer, default=0)
    red_fruit = db.Column(db.Integer, default=0)
    black_fruit = db.Column(db.Integer, default=0)
    total_palm_trees = db.Column(db.Integer, default=0)
    productive_trees = db.Column(db.Integer, default=0)
    unproductive_trees = db.Column(db.Integer, default=0)
    land_area_census = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PalmTree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, inactive, diseased
    productivity = db.Column(db.String(20), default='productive')  # productive, unproductive
    last_census_date = db.Column(db.DateTime)
    health_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
