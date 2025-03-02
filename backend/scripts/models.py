from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
import secrets
import string

# Funkcija za generiranje nasumičnih ID-ova
def generate_random_id(length=10):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(length))

# Funkcija za stvaranje povezanih tablica
def create_association_table(name, col1, col2, for1, for2):
    return db.Table(
        name,
        db.Column(col1, db.Integer, db.ForeignKey(f"{for1}.id"), primary_key=True),
        db.Column(col2, db.Integer, db.ForeignKey(f"{for2}.id"), primary_key=True)
    )

# Definicija povezanih tablica za razne odnose
playlist_audio_association = create_association_table("playlist_audio", "playlist_id", "audio_id", "playlist", "audio")
chat_audio_association = create_association_table("chat_audio", "chat_id", "audio_id", "chat", "audio")
user_playlist_association = create_association_table("user_playlist", "user_id", "playlist_id", "user", "playlist")
user_audio_association = create_association_table("user_audio", "user_id", "audio_id", "user", "audio")
user_following_association = create_association_table("user_following", "user_id", "following_id", "user", "user")
user_follower_association = create_association_table("user_follower", "user_id", "follower_id", "user", "user")

# Osnovni model s zajedničkim poljima za sve entitete
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())  # Datum kreiranja
    is_private = db.Column(db.Boolean, default=False)  # Oznaka da li je predmet privatni

    description = db.Column(db.String(300), nullable=True)  # Opis
    author = db.Column(db.String(50), nullable=False)  # Autor
    listens = db.Column(db.Integer, default=0)  # Broj pregleda
    user_id = db.Column(db.Integer, nullable=False)  # ID korisnika koji je kreirao predmet

# Model za korisnika
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, default=False)  # Admin status

    audios = db.relationship("Audio", secondary=user_audio_association, backref="user")
    playlists = db.relationship("Playlist", secondary=user_playlist_association, backref="user")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    follower_count = db.Column(db.Integer, default=0)  # Broj pratitelja
    overall_listens = db.Column(db.Integer, default=0)  # Ukupno preslušavanja

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

# Model za obavijesti korisnika
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=func.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="notifications")

# Model za audio datoteke
class Audio(BaseModel):
    genre = db.Column(db.String(30), nullable=False)  # Žanr
    file_id = db.Column(db.Integer, nullable=False)  # ID datoteke

# Model za playlistu
class Playlist(BaseModel):  
    audios = db.relationship("Audio", secondary=playlist_audio_association, backref="playlists")

# Model za chat sobe
class Chat(db.Model):
    id = db.Column(db.String(10), primary_key=True, default=generate_random_id, unique=True, nullable=False)  # Jedinstveni ID
    host_id = db.Column(db.Integer, nullable=False)  # ID domaćina chata
    is_private = db.Column(db.Boolean, default=True)  # Da li je chat privatni
    audios = db.relationship("Audio", secondary=chat_audio_association, backref="chats")  # Audio datoteke povezane s chat sobom
