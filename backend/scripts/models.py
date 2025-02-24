from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
import secrets
import string

# 🔹 Utility function for random ID generation
def generate_random_id(length=10):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(length))

# 🔹 Association Tables
def create_association_table(name, col1, col2, for1, for2):
    return db.Table(
        name,
        db.Column(col1, db.Integer, db.ForeignKey(f"{for1}.id"), primary_key=True),
        db.Column(col2, db.Integer, db.ForeignKey(f"{for2}.id"), primary_key=True)
    )

playlist_audio_association = create_association_table("playlist_audio", "playlist_id", "audio_id", "playlist", "audio")
user_playlist_association = create_association_table("user_playlist", "user_id", "playlist_id", "user", "playlist")
user_audio_association = create_association_table("user_audio", "user_id", "audio_id", "user", "audio")
user_following_association = create_association_table("user_following", "user_id", "following_id", "user", "user")
user_follower_association = create_association_table("user_follower", "user_id", "follower_id", "user", "user")

chat_host_association = db.Table(
    "chat_host",
    db.Column("chat_id", db.String(10), db.ForeignKey("chat.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

# 🔹 Base Model for common fields
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    is_private = db.Column(db.Boolean, default=False)

    description = db.Column(db.String(300), nullable=True)
    author = db.Column(db.String(50), nullable=False)
    listens = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)

# 🔹 Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    audios = db.relationship("Audio", secondary=user_audio_association, backref="user")
    playlists = db.relationship("Playlist", secondary=user_playlist_association, backref="user")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    follower_count = db.Column(db.Integer, default=0)
    overall_listens = db.Column(db.Integer, default=0)

    followed = db.relationship(
        "User",
        secondary=user_following_association,
        primaryjoin=id == user_following_association.c.following_id,
        secondaryjoin=id == user_following_association.c.user_id,
    )

    followers = db.relationship(
        "User",
        secondary=user_follower_association,
        primaryjoin=id == user_follower_association.c.user_id,
        secondaryjoin=id == user_follower_association.c.follower_id,
    )

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=func.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="notifications")

class Audio(BaseModel):
    genre = db.Column(db.String(30), nullable=False)
    file_id = db.Column(db.Integer, nullable=False)

class Playlist(BaseModel):  
    audios = db.relationship("Audio", secondary=playlist_audio_association, backref="playlists")

class Chat(db.Model):
    id = db.Column(db.String(10), primary_key=True, default=generate_random_id, unique=True, nullable=False)
    host = db.relationship("User", secondary=chat_host_association, backref="chat")
    is_private = db.Column(db.Boolean, default=True)
