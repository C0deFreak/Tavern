from flask import Blueprint, send_from_directory, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from .models import Audio
from . import db

views = Blueprint('views', __name__)
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@views.route('/index')
@login_required
def index():
    return send_file('../../uploads/1.mp3')

@views.route('/upload', methods=['POST'])
@login_required
def upload():
    name = request.form.get('name')
    description = request.form.get('description')
    genre = request.form.get('genre')
    author = request.form.get('author')

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        new_audio = Audio(name=name, description=description, genre=genre, author=author)
        db.session.add(new_audio)
        db.session.commit()

        filename = secure_filename(f"{new_audio.id}.mp3")
        
        if os.path.splitext(filename)[1] in ['.mp3', '.wav', '.ogg']:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"success": "File uploaded"}), 200
    
    return jsonify({"error": "File upload failed"}), 500

    
