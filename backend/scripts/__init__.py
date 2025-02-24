from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_PARTITIONED'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_PARTITIONED'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

    # Allow credentials (cookies) and specify the allowed origin
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)


    from .views.audio import audio_views
    from .views.common import common_views
    from .views.playlist import playlist_views
    from .views.auth import auth
    from .views.chat import chat_views

    app.register_blueprint(common_views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(audio_views, url_prefix='/audio/')
    app.register_blueprint(playlist_views, url_prefix='/playlist/')
    app.register_blueprint(chat_views, url_prefix='/chat/')


    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('/' + DB_NAME):
        with app.app_context():
            db.create_all()
