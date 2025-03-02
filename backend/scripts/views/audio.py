from ..libraries import *

# Postavljanje Blueprint-a za audio rute
audio_views = Blueprint('audio', __name__)

# Definiranje direktorija za upload audio datoteka
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Osigurava da folder postoji

# ---------------------------------------
# Dohvaća audio datoteku na temelju ID-a
# ---------------------------------------
@audio_views.route('/file/<int:id>')
def get_audio(id):
    audio = Audio.query.get(id)
    if not audio:
        return jsonify({"error": "Audio not found"}), 404
    
    user = User.query.get(audio.user_id)
    
    # Ažuriranje broja preslušavanja
    audio.listens += 1
    user.overall_listens += 1
    db.session.commit()
    
    # Provjera privatnosti i slanje datoteke
    return check_private(item=audio, safe=send_file(f'../uploads/{audio.file_id}.mp3'))

# ---------------------------------------
# Dohvaća informacije o audio zapisu
# ---------------------------------------
@audio_views.route('/info/<int:id>', methods=['GET'])
def get_song(id):
    audio = Audio.query.get(id)
    if not audio:
        return jsonify({"error": "Song not found"}), 404
    
    return check_private(item=audio, safe=jsonify({
        "id": audio.id,
        "name": audio.name,
        "author": audio.author,
        "genre": audio.genre,
        "description": audio.description,
        "is_private": audio.is_private,
        "user_id": audio.user_id,
        "listens": audio.listens
    }))

# ---------------------------------------
# Upload novog audio zapisa
# ---------------------------------------
@audio_views.route('/upload', methods=['POST'])
@login_required
def upload():
    name = request.form.get('name')
    description = request.form.get('description')
    genre = request.form.get('genre')
    private = js_bool_to_py(request.form.get('private'))

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generiranje ID-a za novu audio datoteku
    last_audio = Audio.query.order_by(Audio.id.desc()).first()
    file_id = (last_audio.id + 1) if last_audio else 1
    filename = secure_filename(f"{file_id}.mp3") 

    # Provjera podržanog formata
    if os.path.splitext(filename)[1] not in ['.mp3', '.wav', '.ogg']:
        return jsonify({"error": "Invalid file format"}), 400

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Provjera duplikata
    for audio in os.scandir(UPLOAD_FOLDER):
        if os.path.basename(audio) != filename:
            if open(audio, "rb").read() == open(os.path.join(UPLOAD_FOLDER, filename), "rb").read():
                os.remove(os.path.join(UPLOAD_FOLDER, filename))
                file_id = int(os.path.basename(audio)[:-4])
                break

    # Kreiranje novog audio objekta u bazi
    new_audio = Audio(
        name=name, 
        description=description, 
        genre=genre.lower(), 
        author=current_user.name, 
        is_private=private, 
        user_id=current_user.id, 
        file_id=file_id
    )
    db.session.add(new_audio)
    current_user.audios.append(new_audio)

    # Obavještavanje pratitelja o novom javnom audio zapisu
    if not private:
        for follower in current_user.followers:
            follower.notifications.append(Notification(
                context=f'{current_user.name} published "{name}"!', 
                link=f"{'-'.join(name.split())}_audioid_{new_audio.id}", 
                date=datetime.now()
            ))

    db.session.commit()
    return jsonify({"success": "File uploaded"}), 200

# ---------------------------------------
# Dohvaća popis playlista u kojima se koristi audio
# ---------------------------------------
@audio_views.route('/used_in/<int:id>', methods=['GET'])
@login_required
def get_in_playlists(id):
    if not current_user.playlists:
        return jsonify({"error": "Playlists not found"}), 404

    playlists = [{"id": playlist.id, "name": playlist.name, "used": Audio.query.get(id) in playlist.audios} 
                 for playlist in current_user.playlists]
    
    return jsonify({"used_playlists": playlists})

# ---------------------------------------
# Uređivanje informacija o audio zapisu
# ---------------------------------------
@audio_views.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_audio(id):
    edited_audio = Audio.query.get_or_404(id)
    
    if edited_audio.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    edited_audio.name = request.form.get('name') or edited_audio.name
    edited_audio.description = request.form.get('description') or edited_audio.description
    edited_audio.author = request.form.get('author') or edited_audio.author
    edited_audio.genre = request.form.get('genre') or edited_audio.genre
    edited_audio.is_private = js_bool_to_py(request.form.get('is_private'))

    db.session.commit()
    return jsonify({"success": "Audio edited"}), 200

# ---------------------------------------
# Brisanje audio zapisa
# ---------------------------------------
@audio_views.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_audio(id):
    delete_audio = Audio.query.get_or_404(id)

    if delete_audio.user_id != current_user.id and not current_user.admin:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(delete_audio)

    # Obavještavanje korisnika o brisanju
    user = User.query.get_or_404(delete_audio.user_id)
    user.notifications.append(Notification(
        context="Your audio was deleted because it didn't follow terms and conditions", 
        link="terms-and-conditions", 
        date=datetime.now()
    ))

    db.session.commit()
    return jsonify({"success": "Audio deleted"}), 200

# ---------------------------------------
# Prijava neprikladnog sadržaja
# ---------------------------------------
@audio_views.route('/report/<int:id>', methods=['POST'])
@login_required
def report_audio(id):
    name = request.form.get('name')
    context = request.form.get('context')

    # Slanje obavijesti svim korisnicima na email adresama admina
    for email in email_addresses:
        user = User.query.filter_by(email=email).first()
        if user:
            user.notifications.append(Notification(
                context=f"{name}: {context}", 
                link=f"{'-'.join(name.split())}_audioid_{id}", 
                date=datetime.now()
            ))

    db.session.commit()
    return jsonify({"success": "Audio reported"}), 200
