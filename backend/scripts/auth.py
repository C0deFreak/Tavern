from flask import Blueprint, request, jsonify, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        return jsonify({'message': 'Logged in successfully', 'user': user.email})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(email=email, username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({'message': 'User created successfully'})

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@auth.route('/user')
def user_info():
    if current_user.is_authenticated:
        return jsonify({'message': 'Logged in', 'username': current_user.username})
    else:
        return jsonify({'error': 'Not logged in'}), 400
