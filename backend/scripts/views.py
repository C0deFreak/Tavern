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

def check_private(audio, safe, not_safe={"error": "Song is private"}):
    if audio.is_private and (not current_user.is_authenticated or audio.user_id != current_user.id):
        return jsonify(not_safe), 400
    else:
        return safe
        

@views.route('/index', methods=['POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        quick = request.form.get('quick')
        find_audio = Audio.query.filter(Audio.name.ilike(f'{search}{quick}'))
        audio_files = []

        if find_audio:
            if quick == '%':
                find_audio = find_audio[:3]
            
            audio_files = [{"id": audio.id, "name": audio.name} 
               for audio in find_audio 
               if not audio.is_private or (current_user.is_authenticated and audio.user_id == current_user.id)]


            return jsonify({"audio_files": audio_files}), 200
        else:
            return jsonify({"error": "No audio files found"}), 404
    else:
        return jsonify({"error": "No search term provided"}), 400
        

@views.route('/audio/<int:id>')
def get_audio(id):
    return check_private(audio=Audio.query.get(id), safe=send_file(f'../../uploads/{id}.mp3'))

@views.route('/info/<int:id>', methods=['GET'])
def get_song(id):
    audio = Audio.query.get(id)
    if audio:
        return check_private(audio=audio, safe=jsonify({
            "id": audio.id,
            "name": audio.name,
            "author": audio.author,
            "genre": audio.genre,
            "description": audio.description
        }))
        
    else:
        return jsonify({"error": "Song not found"}), 404
    

@views.route('/upload', methods=['POST'])
@login_required
def upload():
    name = request.form.get('name')
    description = request.form.get('description')
    genre = request.form.get('genre')
    author = request.form.get('author')
    private = request.form.get('private')
    same_files = Audio.query.filter(func.lower(Audio.name) == func.lower(name)).all()

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
                    
    
    if file:
        if private == 'true':
            private = True
        else:
            private = False

        last_audio = Audio.query.order_by(Audio.id.desc()).first()

        filename = secure_filename(f"{(last_audio.id + 1) if last_audio else 1}.mp3")
        
        
        if os.path.splitext(filename)[1] in ['.mp3', '.wav', '.ogg']:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            if same_files:
                for audio in same_files:
                    if (private and (not audio.is_private or audio.user_id == current_user.id)) or (not private and not audio.is_private):
                        os.remove(os.path.join(UPLOAD_FOLDER, filename))
                        return jsonify({"error": "File available"}), 400


                    
            new_audio = Audio(name=name, description=description, genre=genre.lower(), author=author, is_private=private)
            db.session.add(new_audio)
            db.session.commit()
            return jsonify({"success": "File uploaded"}), 200
    
    return jsonify({"error": "File upload failed"}), 500

