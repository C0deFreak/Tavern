import os
from flask import Blueprint, request, redirect, flash, send_from_directory, jsonify
from FlaskBackend.models import Music
from FlaskBackend import db

views = Blueprint('views', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'music_upload')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    global extension
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in ALLOWED_EXTENSIONS

def create_directory(directory='music_upload'):
    if not os.path.exists(directory):
        os.makedirs(directory)

@views.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']
        creator = request.form['creator']
        
        if 'audio_file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['audio_file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            music = Music(name=name, genre=genre, creator=creator, audio_file='')
            db.session.add(music)
            db.session.commit()

            create_directory()

            filename = f"{music.id}.{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            try:
                music.audio_file = filename
                db.session.commit()
            except:
                flash('Uploading error')
                return jsonify({"error": "Uploading error"}), 500
    

@views.route('/music_upload/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@views.route('/music/<string:name>_<int:id>')
def single_music(name, id):
    music = Music.query.get_or_404(id)
    music_data = {
        "id": music.id,
        "name": music.name,
        "genre": music.genre,
        "creator": music.creator,
        "audio_file": music.audio_file
    }
    return jsonify(music_data)  # Return a single object instead of a list
