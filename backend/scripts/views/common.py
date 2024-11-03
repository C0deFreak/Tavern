from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import Audio, Playlist
from ..functions import js_bool_to_py


#SETUP
common_views = Blueprint('common', __name__)

# GLOBAL
# Search for items by getting all items that start with "search"
@common_views.route('/search', methods=['POST'])
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