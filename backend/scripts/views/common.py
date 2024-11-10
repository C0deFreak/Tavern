from ..libraries import *


#SETUP
common_views = Blueprint('common', __name__)

# GLOBAL
# Search for items by getting all items that start with "search"
@common_views.route('/search', methods=['POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        showPrivate = js_bool_to_py(request.form.get('showPrivate'))
        find_audio = db.session.query(Audio.id,
            Audio.name, 
            Audio.is_private, 
            Audio.user_id,
            db.literal('audio').label('type')
            ).filter(Audio.name.ilike(f'{search}%'))

        find_playlist = db.session.query(
            Playlist.id,
            Playlist.name,
            Playlist.is_private, Playlist.user_id,
            db.literal('playlist').label('type')
            ).filter(Playlist.name.ilike(f'{search}%'))
        
        find_user = db.session.query(
            User.id,
            User.username,
            db.literal(0).label('user_id'),
            db.literal(False).label('is_private'),
            db.literal('user').label('type')
            ).filter(User.username.ilike(f'{search}%'))

        find_item = find_audio.union(find_playlist).union(find_user).all()

        if find_item:   
            items = [{"id": item.id, "name": item.name, "item_type": item.type} 
               for item in find_item 
               if not item.is_private or (current_user.is_authenticated and item.user_id == current_user.id and showPrivate)]


            return jsonify({"audio_files": items}), 200
        else:
            return jsonify({"error": "No audio files found"}), 404
    else:
        return jsonify({"error": "No search term provided"}), 400