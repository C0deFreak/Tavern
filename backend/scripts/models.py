from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Definiranje modela korisnika
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150)) 
    audio = db.relationship('Audio') 

# Definiranje modela pojma
class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))