from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS

# Initialize SQLAlchemy object for database operations
db = SQLAlchemy()
DB_NAME = "tavern.db"  # Database name

# Function to create a Flask application
def create_app():
    app = Flask(__name__, template_folder='../Frontend')  # Create a Flask app instance
    app.config['SECRET_KEY'] = 'chamba machamba'  # Secret key for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # URI for SQLite database
    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Configure CORS
    CORS(app, resources={r'/*': {'origins': '*', 'allow_headers': 'Content-Type'}})

    # Import blueprints for views and authentication
    from .views import views
    from .auth import auth

    # Register blueprints with the app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    # Import models
    from .models import User, Music, Playlist

    # Create database if it does not exist
    create_database(app)

    # Initialize LoginManager for managing user sessions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the route for login
    login_manager.init_app(app)

    # Function to load user from the database
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database
def create_database(app):
    if not path.exists('FlaskBackend/' + DB_NAME):  # Check if the database already exists
        with app.app_context():
            db.create_all()  # Create all tables in the database if it does not exist
