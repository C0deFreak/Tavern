from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

playlist_audio_association = db.Table('playlist_audio',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('audio_id', db.Integer, db.ForeignKey('audio.id'), primary_key=True)
)

user_playlist_association = db.Table('user_audio', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    playlists = db.relationship('Playlist', secondary=user_playlist_association, backref='users')

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    genre = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    listens = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    is_private = db.Column(db.Boolean, default=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    date_created = db.Column(db.DateTime, default=func.now())
    listens = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)
    is_private = db.Column(db.Boolean, default=False)
    
    audios = db.relationship('Audio', secondary=playlist_audio_association, backref='playlists')