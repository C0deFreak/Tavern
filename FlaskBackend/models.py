from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Definiranje modela korisnika
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)  # Email korisnika, jedinstveni
    password = db.Column(db.String(150))             # Hashirana lozinka korisnika
    username = db.Column(db.String(150))             # Korisničko ime korisnika
    playlist = db.relationship('Playlist')      # Veza s pojmovima koje je korisnik stvorio

# Definiranje modela pojma
class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)     # Naziv pojma
    genre = db.Column(db.String(30), nullable=False)  # Opis pojma
    creator = db.Column(db.String(30), nullable=False)  # Predmet pojma
    audio_file = db.Column(db.String(100), nullable=False)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    music_ids = db.Column(db.String(1100), nullable=False, default=[])
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

