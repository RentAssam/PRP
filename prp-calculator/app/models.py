from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    basic = db.Column(db.Float, nullable=False)
    da = db.Column(db.Float, nullable=False)
    company_rating = db.Column(db.String(20), nullable=False)
    individual_rating = db.Column(db.Integer, nullable=False)
    employee_type = db.Column(db.String(20), nullable=False)
    profit_met = db.Column(db.Boolean, nullable=False)
    result = db.Column(db.Float, nullable=False)
    tax_impact = db.Column(db.Float, nullable=False)
    projections = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Calculation {self.id}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    employee_id = db.Column(db.String(20), unique=True)
    grade = db.Column(db.String(20))
    department = db.Column(db.String(50))
    calculations = db.relationship('Calculation', backref='author', lazy='dynamic')
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'