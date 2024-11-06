from ..libraries import *


#SETUP
playlist_views = Blueprint('playlist', __name__)

# PLAYLISTS
# Creates the playlists
@playlist_views.route('/create', methods=['POST'])
@login_required
def make_playlist():
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

    return jsonify({"error": "Audio not found"}), 404

#Saved playlists on a account
@playlist_views.route('/saved', methods = ['GET'])
@login_required
def saved_playlists():   
    if current_user.playlists:   
        playlists = [{"id": playlist.id, "name": playlist.name} 
            for playlist in current_user.playlists]

        return jsonify({"playlists": playlists})
    else:
        return jsonify({"error": "Playlists not found"}), 404

# Returns a playlist and its content by its ID    
@playlist_views.route('/info/<int:id>', methods=['GET'])
def get_playlist(id):
    playlist = Playlist.query.get(id)
    if playlist:
        return check_private(item=playlist, safe=jsonify({
            "id": playlist.id,
            "name": playlist.name,
            "author": playlist.author,
            "description": playlist.description,
            "audio_ids" : [audio.id for audio in playlist.audios],
            "is_private" : playlist.is_private,
            "user_id": playlist.user_id
        }))
        
    else:
        return jsonify({"error": "Playlist not found"}), 404

# Edits the content of a playlist (adds or removes audio)    
@playlist_views.route('/edit_content/<int:playlist_id>/<int:id>', methods=['POST'])
@login_required
def edit_playlist_content(playlist_id, id):
    edited_playlist = Playlist.query.get_or_404(playlist_id)
    audio = Audio.query.get_or_404(id)
    if audio in edited_playlist.audios:
        edited_playlist.audios.remove(audio)
    else:
        edited_playlist.audios.append(audio)
        
    db.session.commit()
    return jsonify({"success": "Playlist edited"}), 200

# Edits the playlist info   
@playlist_views.route('/edit/int:id>', methods=['POST'])
@login_required
def edit_playlist(id):
    edited_playlist = Playlist.query.get_or_404(id)
    name = request.form.get('name')
    description = request.form.get('description')
    is_private = js_bool_to_py(request.form.get('is_private'))
    
    if name:
        edited_playlist.name = name
        edited_playlist.description = description
        edited_playlist.is_private = is_private
        
        db.session.commit()
        return jsonify({"success": "Playlist edited"}), 200

    return jsonify({"error": "Playlist edit failed"}), 500
