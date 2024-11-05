from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from ..models import Audio
from .. import db
from ..functions import check_private, js_bool_to_py
import json

#SETUP
audio_views = Blueprint('audio', __name__)
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# AUDIO
# Returns the audio file (.mp3)
@audio_views.route('/file/<int:id>')
def get_audio(id):
    audio = Audio.query.get(id)
    return check_private(item=audio, safe=send_file(f'../uploads/{audio.file_id}.mp3'))


# Returns audio info by its ID
@audio_views.route('/info/<int:id>', methods=['GET'])
def get_song(id):
    audio = Audio.query.get(id)
    if audio:
        return check_private(item=audio, safe=jsonify({
            "id": audio.id,
            "name": audio.name,
            "author": audio.author,
            "genre": audio.genre,
            "description": audio.description,
            "is_private": audio.is_private,
            "user_id": audio.user_id
        }))
        
    else:
        return jsonify({"error": "Song not found"}), 404

# Creates the audio, adds it to the database
@audio_views.route('/upload', methods=['POST'])
@login_required
def upload():
    name = request.form.get('name')
    description = request.form.get('description')
    genre = request.form.get('genre')
    author = request.form.get('author')
    private = js_bool_to_py(request.form.get('private'))
    file_id = 1

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
                    
    
    if file:
        last_audio = Audio.query.order_by(Audio.id.desc()).first()

        file_id = (last_audio.id + 1) if last_audio else 1
        filename = secure_filename(f"{file_id}.mp3") 
        
        if os.path.splitext(filename)[1] in ['.mp3', '.wav', '.ogg']:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            for audio in os.scandir(UPLOAD_FOLDER):
                if os.path.basename(audio) != filename:
                    if open(audio, "rb").read() == open(os.path.join(UPLOAD_FOLDER, filename), "rb").read():
                        os.remove(os.path.join(UPLOAD_FOLDER, filename))
                        file_id = int(os.path.basename(audio)[:-4])
                        break

                    
            new_audio = Audio(name=name, description=description, genre=genre.lower(), author=author, is_private=private, user_id=current_user.id, file_id=file_id)
            db.session.add(new_audio)
            db.session.commit()
            return jsonify({"success": "File uploaded"}), 200
    
    return jsonify({"error": "File upload failed"}), 500

# Returns all playlists that have this song
@audio_views.route('/used_in/<int:id>', methods=['GET'])
@login_required
def get_in_playlists(id):
    if current_user.playlists: 
        playlists = [{"id": playlist.id, "name": playlist.name, "used": Audio.query.get(id) in playlist.audios} 
            for playlist in current_user.playlists ]
        
        return jsonify({"used_playlists": playlists})
    else:
        return jsonify({"error": "Playlists not found"}), 404
    
# Edits the audio info   
@audio_views.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_audio(id):
    edited_audio = Audio.query.get_or_404(id)
    name = request.form.get('name')
    description = request.form.get('description')
    author = request.form.get('author')
    genre = request.form.get('genre')
    is_private = js_bool_to_py(request.form.get('is_private'))
    
    if name:
        edited_audio.name = name
        edited_audio.description = description
        edited_audio.is_private = is_private
        edited_audio.author = author
        edited_audio.genre = genre
        
        db.session.commit()
        return jsonify({"success": "Audio edited"}), 200

    return jsonify({"error": "Audio edit failed"}), 500