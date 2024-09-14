from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    genre = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    listens = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)


