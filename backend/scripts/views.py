from flask import Blueprint, send_from_directory, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from .models import Audio
from . import db
from sqlalchemy.sql import func

views = Blueprint('views', __name__)
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@views.route('/index', methods=['POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        quick = request.form.get('quick')
        find_audio = Audio.query.filter(Audio.name.ilike(f'{search}{quick}'))

        if find_audio:
            if quick == '%':
                audio_files = [{"id": audio.id, "name": audio.name} for audio in find_audio[:3]]
            else:
                audio_files = [{"id": audio.id, "name": audio.name} for audio in find_audio]
            return jsonify({"audio_files": audio_files}), 200
        else:
            return jsonify({"error": "No audio files found"}), 404
    else:
        return jsonify({"error": "No search term provided"}), 400
        

@views.route('/audio/<int:id>')
def get_audio(id):
    return send_file(f'../../uploads/{id}.mp3')

@views.route('/info/<int:id>', methods=['GET'])
def get_song(id):
    audio = Audio.query.get(id)
    if audio:
        return jsonify({
            "id": audio.id,
            "name": audio.name,
            "author": audio.author,
            "genre": audio.genre,
            "description": audio.description
        })
    else:
        return jsonify({"error": "Song not found"}), 404

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
        new_audio = Audio(name=name, description=description, genre=genre.lower(), author=author)
        db.session.add(new_audio)
        db.session.commit()

        filename = secure_filename(f"{new_audio.id}.mp3")
        
        if os.path.splitext(filename)[1] in ['.mp3', '.wav', '.ogg']:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"success": "File uploaded"}), 200
    
    return jsonify({"error": "File upload failed"}), 500

