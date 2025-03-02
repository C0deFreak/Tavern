from ..libraries import *

# Blueprint za autentifikaciju
auth = Blueprint('auth', __name__)

# ---------------------------------------
# Login korisnika
# ---------------------------------------
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Dohvaća JSON podatke iz zahtjeva
    email = data.get('email')  # Email korisnika
    password = data.get('password')  # Lozinka korisnika

    user = User.query.filter_by(email=email).first()  # Provjera korisnika u bazi prema emailu
    if user and check_password_hash(user.password, password):  # Provjera lozinke
        login_user(user, remember=True)  # Prijava korisnika
        return jsonify({'message': 'Logged in successfully', 'user': user.email})
    return jsonify({'error': 'Invalid credentials'}), 401  # Ako nije ispravno, vraća grešku

# ---------------------------------------
# Registracija novog korisnika
# ---------------------------------------
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Dohvaća JSON podatke iz zahtjeva
    email = data.get('email')  # Email korisnika
    name = data.get('name')  # Ime korisnika
    password = data.get('password')  # Lozinka korisnika

    # Provjera da li email već postoji u bazi
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400  # Greška ako email postoji

    # Provjera da li je korisnik admin (prema email adresama)
    return_admin_emails()
    new_user = User(
        email=email, 
        name=name, 
        password=generate_password_hash(password), 
        admin=True if email in email_addresses else False
    )
    db.session.add(new_user)  # Dodavanje korisnika u bazu
    db.session.commit()

    login_user(new_user)  # Automatska prijava nakon registracije
    return jsonify({'message': 'User created successfully'})

# ---------------------------------------
# Logout korisnika
# ---------------------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Odjava korisnika
    return jsonify({'message': 'Logged out successfully'})

# ---------------------------------------
# Provjera trenutnog korisnika
# ---------------------------------------
@auth.route('/user_check')
def check_current_user():
    if current_user.is_authenticated:  # Provjera je li korisnik prijavljen
        return jsonify({
            'message': 'Logged in',
            'name': current_user.name,
            'id': current_user.id,
            'admin': current_user.admin
        })
    else:
        return jsonify({'error': 'Not logged in'}), 400  # Ako nije prijavljen, vraća grešku

# ---------------------------------------
# Dohvaća informacije o korisniku na temelju ID-a
# ---------------------------------------
@auth.route('/info/<int:id>', methods=['GET'])
def get_any_user(id):
    user = User.query.get_or_404(id)  # Dohvaća korisnika prema ID-u, ili 404 ako ne postoji
    if user:
        return jsonify({
            'name': user.name,
            'id': user.id,
            "playlists": [playlist.id for playlist in user.playlists if (user == current_user) or (not playlist.is_private)],
            "audios": [audio.id for audio in user.audios if (user == current_user) or (not audio.is_private)],
            "followed": [followed.id for followed in user.followed],
            "listens": user.overall_listens, 
            "followers": user.follower_count,
            "is_following": current_user.is_authenticated and current_user in user.followers        
        })
    else:
        return jsonify({'error': 'User not found'}), 404  # Ako korisnik nije pronađen, vraća grešku

# ---------------------------------------
# Funkcija za praćenje ili prestanak praćenja korisnika
# ---------------------------------------
@auth.route('/follow/<int:id>', methods=['POST'])
def follow_user(id):
    user = User.query.get_or_404(id)  # Dohvaća korisnika prema ID-u
    if user:
        if user not in current_user.followed:  # Ako još ne prati korisnika
            current_user.followed.append(user)  # Dodaj u listu pratitelja
            user.followers.append(current_user)  # Dodaj trenutnog korisnika kao pratitelja
            user.follower_count += 1  # Povećaj broj pratitelja
            user.notifications.append(Notification(
                context=f"{current_user.name} followed you!", 
                link=f"{'-'.join((current_user.name).split())}_userid_{current_user.id}", 
                date=datetime.now()
            ))
            db.session.commit()
            return jsonify({'message': 'Followed successfully'})
        else:
            current_user.followed.remove(user)  # Ukloni iz liste pratitelja
            user.followers.remove(current_user)  # Ukloni trenutnog korisnika iz liste pratitelja
            user.follower_count -= 1  # Smanji broj pratitelja
            db.session.commit()
            return jsonify({'message': 'Unfollowed successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404  # Ako korisnik nije pronađen, vraća grešku

# ---------------------------------------
# Dohvaća obavijesti za trenutnog korisnika
# ---------------------------------------
@auth.route('/notifications', methods=['GET'])
@login_required
def notifications():
    # Ispisivanje obavijesti za trenutnog korisnika
    return jsonify({
        "context": [notify.context for notify in current_user.notifications],
        "link": [notify.link for notify in current_user.notifications],
        "date": [notify.date for notify in current_user.notifications]
    })
