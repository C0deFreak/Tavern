from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chamba machamba'
     # Configure session cookies for local development
     # Make sure that domains are the same (for example localhost)
    app.config['SESSION_COOKIE_SAMESITE'] = None # Allow cross-site cookies
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_DOMAIN'] = None  # No domain setting for local development
    app.config.update()

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}) #DONT PUT / ON THE END OF THE LINK
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)


    from .views.audio import audio_views
    from .views.common import common_views
    from .views.playlist import playlist_views
    from .views.auth import auth

    app.register_blueprint(common_views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(audio_views, url_prefix='/audio/')
    app.register_blueprint(playlist_views, url_prefix='/playlist/')


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
