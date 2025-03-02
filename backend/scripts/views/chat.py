from ..libraries import *
from scripts.socketio_instance import socketio

# Blueprint za chat funkcionalnost
chat_views = Blueprint("chat", __name__)

# ---------------------------------------
# Kreiranje nove chat sobe
# ---------------------------------------
@chat_views.route("/create", methods=["POST"])
@login_required
def make_chat():
    new_chat = Chat(host_id=current_user.id)  # Kreira novu chat sobu s trenutnim korisnikom kao hostom
    db.session.add(new_chat)  # Dodavanje nove sobe u bazu
    db.session.commit()  # Potvrda promjena u bazi
    return jsonify({"code": new_chat.id})  # Vraća ID nove sobe

# ---------------------------------------
# Dohvaća informacije o chat sobi
# ---------------------------------------
@chat_views.route("/<string:id>", methods=["GET"])
def chat_room(id):
    chat = Chat.query.get(id)  # Dohvaća chat sobu prema ID-u
    if chat:
        return jsonify({"host": chat.host_id, "audio_ids" : [audio.id for audio in chat.audios]})
    else:
        return jsonify({"error": "Room not found"}), 404  # Ako chat soba nije pronađena, vraća grešku

# ---------------------------------------
# Dodavanje audio datoteke u chat sobu
# ---------------------------------------
@chat_views.route('/<string:id>/add', methods=['POST'])
def add_audio(id):
    added_audio = request.form.get('change_audio')  # Dohvaća ID audio datoteke
    chat = Chat.query.get_or_404(id)  # Dohvaća chat sobu prema ID-u, ili vraća grešku
    audio = Audio.query.get_or_404(added_audio)  # Dohvaća audio datoteku prema ID-u, ili vraća grešku
    if chat and audio:
        chat.audios.append(audio)  # Dodavanje audio datoteke u chat sobu
        db.session.commit()  # Potvrda promjena u bazi
        return jsonify({"success": "added audio"}), 200  # Vraća uspješan odgovor
    else:
        return jsonify({"error": "Can't add audio"}), 404  # Ako chat ili audio nisu pronađeni, vraća grešku

# ---------------------------------------
# Uklanjanje audio datoteke iz chat sobe
# ---------------------------------------
@chat_views.route('/<string:id>/remove', methods=['POST'])
def remove_audio(id):
    removed_audio = request.form.get('change_audio')  # Dohvaća ID audio datoteke
    chat = Chat.query.get_or_404(id)  # Dohvaća chat sobu prema ID-u, ili vraća grešku
    audio = Audio.query.get_or_404(removed_audio)  # Dohvaća audio datoteku prema ID-u, ili vraća grešku
    if chat and audio:
        chat.audios.remove(audio)  # Uklanjanje audio datoteke iz chat sobe
        db.session.commit()  # Potvrda promjena u bazi
        return jsonify({"success": "removed audio"}), 200  # Vraća uspješan odgovor
    else:
        return jsonify({"error": "Can't add audio"}), 404  # Ako chat ili audio nisu pronađeni, vraća grešku

# ---------------------------------------
# Obrađuje zahtjev za ulazak u chat sobu
# ---------------------------------------
@socketio.on("join")
def handle_join(data):
    room = data["room"]  # Dohvaća ID sobe
    join_room(room)  # Korisnik ulazi u sobu
    emit("message", {"user": "System", "message": f"{current_user.name} has joined."}, room=room)  # Obavještava ostale korisnike da je korisnik ušao u sobu

# ---------------------------------------
# Obrađuje zahtjev za napuštanje chat sobe
# ---------------------------------------
@socketio.on("leave")
def handle_leave(data):
    room = data["room"]  # Dohvaća ID sobe
    left_user = data["id"]  # Dohvaća ID korisnika koji napušta sobu
    
    # Dohvaća chat prema ID-u sobe
    chat = Chat.query.get(room)
    
    if chat:
        # Ako korisnik koji napušta sobu je host, soba će biti obrisana
        if left_user == chat.host_id:
            db.session.delete(chat)  # Briše chat iz baze
            db.session.commit()  # Potvrda promjena u bazi
            emit("message", {"user": "System", "message": "Host has left. The room is being deleted."}, room=room)
        else:
            emit("message", {"user": "System", "message": f"{current_user.name} has left."}, room=room)
    leave_room(room)  # Korisnik napušta sobu

# ---------------------------------------
# Obrađuje slanje poruka u chat sobu
# ---------------------------------------
@socketio.on("send_message")
def handle_message(data):
    room = data["room"]  # Dohvaća ID sobe
    message = data["message"]  # Dohvaća poruku
    emit("message", {"user": current_user.name, "message": message}, room=room)  # Šalje poruku svim korisnicima u sobi

# ---------------------------------------
# Obrađuje play_audio događaj
# ---------------------------------------
@socketio.on("play_audio")
def handle_play_audio(data):
    room = data["room"]  # Dohvaća ID sobe
    audioInfos = data["audioInfos"]  # Dohvaća informacije o audio datotekama
    
    # Šalje play_audio događaj svim korisnicima u sobi
    emit("play_audio", {"room": room, "audioInfos": audioInfos}, room=room)
