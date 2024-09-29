from flask import Blueprint, send_from_directory, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from .models import Audio, Playlist
from . import db
from sqlalchemy.sql import func
import json

#SETUP
views = Blueprint('views', __name__)
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# OPTIMIZATION
# Functions that shorten the repeated code
def check_private(item, safe, not_safe={"error": "Item is private"}):
    if item.is_private and (not current_user.is_authenticated or item.user_id != current_user.id):
        if not_safe == {"error": "Item is private"}:
            return jsonify(not_safe), 400
        else:
            return not_safe
    else:
        return safe
    
def js_bool_to_py(translate):
    if translate == 'true':
            return True
    else:
        return False
        

# GLOBAL
# Search for items by getting all items that start with "search"
@views.route('/search', methods=['POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        showPrivate = js_bool_to_py(request.form.get('showPrivate'))
        find_audio = Audio.query.filter(Audio.name.ilike(f'{search}%')) 

        if find_audio:   
            audio_files = [{"id": audio.id, "name": audio.name} 
               for audio in find_audio 
               if not audio.is_private or (current_user.is_authenticated and audio.user_id == current_user.id and showPrivate)]


            return jsonify({"audio_files": audio_files}), 200
        else:
            return jsonify({"error": "No audio files found"}), 404
    else:
        return jsonify({"error": "No search term provided"}), 400


# AUDIO
# Returns the audio and its information
@views.route('/audio/<int:id>')
def get_audio(id):
    audio = Audio.query.get(id)
    return check_private(item=audio, safe=send_file(f'../../uploads/{audio.file_id}.mp3'))

@views.route('/info/<int:id>', methods=['GET'])
def get_song(id):
    audio = Audio.query.get(id)
    if audio:
        return check_private(item=audio, safe=jsonify({
            "id": audio.id,
            "name": audio.name,
            "author": audio.author,
            "genre": audio.genre,
            "description": audio.description
        }))
        
    else:
        return jsonify({"error": "Song not found"}), 404

# Creates the audio
@views.route('/upload', methods=['POST'])
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
                        print('ođe')
                        break

                    
            new_audio = Audio(name=name, description=description, genre=genre.lower(), author=author, is_private=private, user_id=current_user.id, file_id=file_id)
            db.session.add(new_audio)
            db.session.commit()
            return jsonify({"success": "File uploaded"}), 200
    
    return jsonify({"error": "File upload failed"}), 500


# PLAYLISTS
# Creates the playlists
@views.route('/make_playlist', methods=['POST'])
@login_required
def mk_playlist():
    name = request.form.get('name')
    description = request.form.get('description')
    private = js_bool_to_py(request.form.get('private'))
    added_audio_json = request.form.get('added_audio')

    new_playlist = Playlist(name=name, description=description, is_private=private, user_id=current_user.id, author=current_user.username)
    db.session.add(new_playlist)
    db.session.commit()

    if added_audio_json:
        added_audio = json.loads(added_audio_json)
        added_audio= Audio.query.filter(Audio.id.in_(added_audio)).all()
        new_playlist.audios.extend(added_audio)
        current_user.playlists.append(new_playlist)
        db.session.commit()

    return jsonify({"success": "Playlist made"}), 200

#Saved playlists
@views.route('/saved', methods = ['GET'])
@login_required
def saved_playlists():   
    if current_user.playlists:   
        playlists = [{"id": playlist.id, "name": playlist.name} 
            for playlist in current_user.playlists 
            if not playlist.is_private or playlist.user_id == current_user.id]

        return jsonify({"playlists": playlists})
    else:
        return jsonify({"error": "Playlists not found"}), 404
    
@views.route('/playlist/<int:id>', methods=['GET'])
def get_playlist(id):
    playlist = Playlist.query.get(id)
    if playlist:
        return check_private(item=playlist, safe=jsonify({
            "id": playlist.id,
            "name": playlist.name,
            "author": playlist.author,
            "description": playlist.description,
            "audio_ids" : [audio.id for audio in playlist.audios]
        }))
        
    else:
        return jsonify({"error": "Playlist not found"}), 404