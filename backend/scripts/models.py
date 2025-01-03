from . import db
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

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    audios = db.relationship('Audio', secondary=user_audio_association, backref='users')
    playlists = db.relationship('Playlist', secondary=user_playlist_association, backref='users')
    
    # Self-referential relationship for followers
    followed = db.relationship(
        'User',
        secondary=user_following_association,
        primaryjoin=id == user_following_association.c.following_id,
        secondaryjoin=id == user_following_association.c.user_id,
        backref='following'
    )

    @hybrid_property
    def listens(self):
        # Sum the listens of all related Audio records
        return sum(audio.listens for audio in self.audios)

    @listens.expression
    def listens(cls):
        # Generate a SQL expression to sum listens for each User
        return (
            db.select([func.sum(Audio.listens)])
            .where(Audio.id.in_(
                db.select([user_audio_association.c.audio_id])
                .where(user_audio_association.c.user_id == cls.id)
            ))
            .label("listens")
        )

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
