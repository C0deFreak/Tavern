from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Blueprint for authentication
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Parse JSON data
    
        email = data.get('email')
        password = data.get('password')

        logging.debug(f"Attempting login for email: {email}")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            logging.debug(f"Login successful for email: {email}")
            return jsonify({"success": True, "message": "Successfully logged in"})
        else:
            logging.debug(f"Login failed for email: {email}")
            return jsonify({"success": False, "message": "Invalid email or password"})

    return jsonify({"success": False, "message": "Invalid request method"})

@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return jsonify({"success": True, "message": "Successfully logged out"}), 200

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()  # Parse JSON data
    
        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        logging.debug(f"Attempting sign-up for email: {email}")

        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({"success": False, "message": "User already exists"})
        elif len(email) < 4:
            return jsonify({"success": False, "message": "Invalid email"})
        elif len(username) < 2:
            return jsonify({"success": False, "message": "Username too short"})
        elif password1 != password2:
            return jsonify({"success": False, "message": "Passwords do not match"})
        elif len(password1) < 7:
            return jsonify({"success": False, "message": "Password too short"})
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            logging.debug(f"Sign-up successful for email: {email}")
            return jsonify({"success": True, "message": "Successfully signed up"})

    return jsonify({"success": False, "message": "Invalid request method"})

@auth.route('/user_info', methods=['GET'])
@login_required
def user_info():
    logging.debug(f"Request method: {request.method}")
    logging.debug(f"Current user: {current_user}")

    user_info = {
        "email": current_user.email,
        "username": current_user.username
    }
    return jsonify(user_info)
