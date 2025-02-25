from ..libraries import *


#SETUP
chat_views = Blueprint('chat', __name__)

# PLAYLISTS
# Creates the playlists
@chat_views.route('/create', methods=['POST'])
@login_required
def make_chat():
    new_chat = Chat(host_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"code": new_chat.id})


@chat_views.route('/<string:id>', methods=['GET'])
def chat_room(id):
    chat = Chat.query.get(id)
    if chat:
        return jsonify({"host": chat.host_id})
    else:
        return jsonify({"error": "Room not found"}), 404
    
@chat_views.route('/<string:id>/add', methods=['POST'])
def add_audio(id):
    added_audio = request.form.get('change_audio')
    print(added_audio)
    chat = Chat.query.get_or_404(id)
    audio = Audio.query.get_or_404(added_audio)
    if chat and audio:
        chat.audios.append(audio)
        db.session.commit()
        return jsonify({"success": "added audio"}), 200
    else:
        return jsonify({"error": "Can't add audio"}), 404
    
@chat_views.route('/<string:id>/remove', methods=['POST'])
def remove_audio(id):
    removed_audio = request.form.get('change_audio')
    chat = Chat.query.get_or_404(id)
    audio = Audio.query.get_or_404(removed_audio)
    if chat and audio:
        chat.audios.remove(audio)
        db.session.commit()
        return jsonify({"success": "removed audio"}), 200
    else:
        return jsonify({"error": "Can't add audio"}), 404