from ..libraries import *
from scripts.socketio_instance import socketio

chat_views = Blueprint("chat", __name__)

@chat_views.route("/create", methods=["POST"])
@login_required
def make_chat():
    new_chat = Chat(host_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"code": new_chat.id})

@chat_views.route("/<string:id>", methods=["GET"])
def chat_room(id):
    chat = Chat.query.get(id)
    if chat:
        return jsonify({"host": chat.host_id, "audio_ids" : [audio.id for audio in chat.audios]})
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

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("message", {"user": "System", "message": f"{current_user.name} has joined."}, room=room)

@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    leave_room(room)
    emit("message", {"user": "System", "message": f"{current_user.name} has left."}, room=room)

@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    message = data["message"]
    emit("message", {"user": current_user.name, "message": message}, room=room)
