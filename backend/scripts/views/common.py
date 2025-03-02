from ..libraries import *

# Blueprint za zajedničke (common) funkcionalnosti
common_views = Blueprint('common', __name__)

# Pokreće funkciju koja vraća administrativne email adrese (verificira administratore)
return_admin_emails()

# ---------------------------------------
# Pretraga stavki (audio, playlist, korisnici) na temelju imena
# ---------------------------------------
@common_views.route('/search', methods=['POST'])
def index():
    if request.method == 'POST':
        # Dohvatanje korisničkog unosa
        search = request.form.get('search')
        songs_only = js_bool_to_py(request.form.get('songs_only'))
        showPrivate = js_bool_to_py(request.form.get('showPrivate'))  # Provjera hoće li se prikazivati privatne stavke

        # Pretraga audio datoteka prema imenu (korištenje 'ilike' za pretragu koja je neosjetljiva na velika i mala slova)
        find_audio = db.session.query(Audio.id, Audio.name, Audio.is_private, Audio.user_id, db.literal('audio').label('type')) \
            .filter(Audio.name.ilike(f'{search}%'))

        if not songs_only:
            # Pretraga playlisti prema imenu
            find_playlist = db.session.query(Playlist.id, Playlist.name, Playlist.is_private, Playlist.user_id, db.literal('playlist').label('type')) \
                .filter(Playlist.name.ilike(f'{search}%'))

            # Pretraga korisnika prema imenu
            find_user = db.session.query(User.id, User.name, db.literal(0).label('user_id'), db.literal(False).label('is_private'), db.literal('user').label('type')) \
                .filter(User.name.ilike(f'{search}%'))

            # Kombiniranje rezultata svih pretraga (audio, playlist, korisnici)
            find_item = find_audio.union(find_playlist).union(find_user).all()
        
        else:
            find_item = find_audio

        # Ako su pronađeni rezultati, filtriraj i prikaži samo one koji su vidljivi (ako je korisnik autentificiran i ako može vidjeti privatne stavke)
        if find_item:
            items = [{"id": item.id, "name": item.name, "item_type": item.type}
                     for item in find_item
                     if not item.is_private or (current_user.is_authenticated and item.user_id == current_user.id and showPrivate)]

            # Vraća sve odgovarajuće stavke u JSON formatu
            return jsonify({"audio_files": items}), 200
        else:
            # Ako nisu pronađeni rezultati, vraća grešku
            return jsonify({"error": "No audio files found"}), 404
    else:
        # Ako nije dostavljen termin za pretragu, vraća grešku
        return jsonify({"error": "No search term provided"}), 400
