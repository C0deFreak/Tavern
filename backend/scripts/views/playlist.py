from ..libraries import *

# Blueprint za funkcionalnosti vezane uz playlistu
playlist_views = Blueprint('playlist', __name__)

# ---------------------------------------
# Kreira novu playlistu
# ---------------------------------------
@playlist_views.route('/create', methods=['POST'])
@login_required
def make_playlist():
    # Dohvaćanje podataka o novoj playlisti
    name = request.form.get('name')
    description = request.form.get('description')
    private = js_bool_to_py(request.form.get('private'))
    added_audio_json = request.form.get('added_audio')

    # Kreiranje nove playliste
    new_playlist = Playlist(name=name, description=description, is_private=private, user_id=current_user.id, author=current_user.name)
    db.session.add(new_playlist)
    db.session.commit()

    # Ako su dodana audio djela, poveži ih s playlistom
    if added_audio_json:
        added_audio = json.loads(added_audio_json)
        added_audio = Audio.query.filter(Audio.id.in_(added_audio)).all()
        new_playlist.audios.extend(added_audio)  # Dodaj audio djela u playlistu
        current_user.playlists.append(new_playlist)  # Dodaj playlistu korisniku
        db.session.commit()

        return jsonify({"success": "Playlist made"}), 200

    return jsonify({"error": "Audio not found"}), 404

# ---------------------------------------
# Vraća spremljene playlistu korisnika
# ---------------------------------------
@playlist_views.route('/saved', methods = ['GET'])
@login_required
def saved_playlists():
    if current_user.playlists:
        playlists = [{"id": playlist.id, "name": playlist.name} 
            for playlist in current_user.playlists]

        return jsonify({"playlists": playlists})
    else:
        return jsonify({"error": "Playlists not found"}), 404

# ---------------------------------------
# Vraća detalje o playlisti
# ---------------------------------------
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

# ---------------------------------------
# Uređuje sadržaj playliste (dodaje ili uklanja audio)
# ---------------------------------------
@playlist_views.route('/edit_content/<int:playlist_id>/<int:id>', methods=['POST'])
@login_required
def edit_playlist_content(playlist_id, id):
    edited_playlist = Playlist.query.get_or_404(playlist_id)
    audio = Audio.query.get_or_404(id)
    if edited_playlist.user_id == current_user.id:
        # Dodavanje ili uklanjanje audio djela iz playliste
        if audio in edited_playlist.audios:
            edited_playlist.audios.remove(audio)
        else:
            edited_playlist.audios.append(audio)
            
        db.session.commit()
        return jsonify({"success": "Playlist edited"}), 200
    
    return jsonify({"error": "Playlist edit failed"}), 500

# ---------------------------------------
# Uređuje osnovne informacije o playlisti
# ---------------------------------------
@playlist_views.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_playlist(id):
    edited_playlist = Playlist.query.get_or_404(id)
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name and edited_playlist.user_id == current_user.id:
        edited_playlist.name = name
        edited_playlist.description = description
       
        db.session.commit()
        return jsonify({"success": "Playlist edited"}), 200

    return jsonify({"error": "Playlist edit failed"}), 500

# ---------------------------------------
# Briše playlistu
# ---------------------------------------
@playlist_views.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_playlist(id):
    delete_playlist = Playlist.query.get_or_404(id)
    
    if delete_playlist.user_id == current_user.id:
        db.session.delete(delete_playlist)  # Briše playlistu iz baze
        db.session.commit()
        return jsonify({"success": "Playlist deleted"}), 200

    return jsonify({"error": "Playlist delete failed"}), 500
