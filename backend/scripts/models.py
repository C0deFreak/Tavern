from . import db
from datetime import datetime
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

# Association tables
playlist_audio_association = db.Table('playlist_audio',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('audio_id', db.Integer, db.ForeignKey('audio.id'), primary_key=True)
)

user_playlist_association = db.Table('user_playlist', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
)

user_audio_association = db.Table('user_audio', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('audio_id', db.Integer, db.ForeignKey('audio.id'), primary_key=True),
)

user_following_association = db.Table('user_following', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),  # The user being followed
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)  # The follower
)

user_follower_association = db.Table('user_follower', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),  # The user being followed
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)  # The follower
)

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    audios = db.relationship('Audio', secondary=user_audio_association, backref='user')
    playlists = db.relationship('Playlist', secondary=user_playlist_association, backref='user')
    follower_count = db.Column(db.Integer, default=0)
    overall_listens = db.Column(db.Integer, default=0)
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    
    # Self-referential relationship for followers
    followed = db.relationship(
        'User',
        secondary=user_following_association,
        primaryjoin=id == user_following_association.c.following_id,
        secondaryjoin=id == user_following_association.c.user_id,
    )

    followers = db.relationship(
        'User',
        secondary=user_follower_association,
        primaryjoin=id == user_follower_association.c.user_id,
        secondaryjoin=id == user_follower_association.c.follower_id,
    )
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each notification
    context = db.Column(db.String(255), nullable=False)  # Text of the notification
    link = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime, nullable=False)  # Timestamp of the notification

    # Assuming notifications are linked to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User table
    user = db.relationship('User', back_populates='notifications')  # Relationship with User

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    genre = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    listens = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    file_id = db.Column(db.Integer, nullable=False)
    is_private = db.Column(db.Boolean, default=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    author = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    listens = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)
    is_private = db.Column(db.Boolean, default=False)
    
    audios = db.relationship('Audio', secondary=playlist_audio_association, backref='playlists')
